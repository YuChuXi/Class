import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import re

# 数据库初始化
Base = declarative_base()
engine = db.create_engine('sqlite:///car_rental.db')
Session = sessionmaker(bind=engine)
session = Session()

# 输入验证函数
def validate_car_id(car_id):
    """验证车牌号格式（至少包含1个字母和1个数字）"""
    if not re.match(r'^.*[A-Za-z].*[0-9].*$', car_id):
        raise ValueError("车牌号必须包含字母和数字")
    return car_id

def validate_positive_number(value, name="数值"):
    """验证正数"""
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"{name}必须大于0")
        return num
    except ValueError:
        raise ValueError(f"无效的{name}")

def validate_integer(value, name="数值"):
    """验证正整数"""
    try:
        num = int(value)
        if num <= 0:
            raise ValueError(f"{name}必须大于0")
        return num
    except ValueError:
        raise ValueError(f"无效的{name}")

def validate_contact(contact):
    """验证联系方式（至少6位数字）"""
    if not re.match(r'^\d{6,}$', contact):
        raise ValueError("联系方式必须至少包含6位数字")
    return contact

def validate_date(date_str):
    """验证日期格式（YYYY-MM-DD）"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("日期格式不正确，应为YYYY-MM-DD")

def get_valid_input(prompt, validator, default=None, is_optional=False):
    """获取有效输入"""
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default
            if not value and is_optional:
                return None
            if not value:
                raise ValueError("输入不能为空")
            return validator(value)
        except ValueError as e:
            print(f"错误: {e}，请重新输入")

class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True)
    car_id = Column(String(20), unique=True)  # 车牌号
    rented = Column(Boolean, default=False)  # 租借状态
    day_charge = Column(Float)  # 日租金
    deposit = Column(Float)  # 押金
    renter = Column(String(50), nullable=True)  # 租借人
    renter_contact = Column(String(20), nullable=True)  # 租借人电话
    date_rent = Column(Date, nullable=True)  # 租借日期
    date_return = Column(Date, nullable=True)  # 归还日期
    brand = Column(String(50))  # 品牌
    type = Column(String(20))  # 车辆类型
    
    __mapper_args__ = {
        'polymorphic_identity': 'car',
        'polymorphic_on': type
    }
    
    def __str__(self):
        msg = [
            f"车牌号: {self.car_id}",
            f"品牌: {self.brand}",
            f"类型: {self.type}",
            f"日租金: {self.day_charge}元",
            f"押金: {self.deposit}元",
            f"租借状态: {'已租出' if self.rented else '可租借'}"
        ]
        if self.rented:
            msg.extend([
                f"租借人: {self.renter}",
                f"联系方式: {self.renter_contact}",
                f"租借日期: {self.date_rent}",
                f"归还日期: {self.date_return if self.date_return else '未归还'}"
            ])
        return "\n".join(msg)

# 7座及以下轿车
class Sedan(Car):
    __tablename__ = 'sedans'
    
    id = Column(Integer, db.ForeignKey('cars.id'), primary_key=True)
    seats = Column(Integer)  # 座位数
    
    __mapper_args__ = {
        'polymorphic_identity': 'sedan',
    }
    
    def __init__(self, car_id, brand, seats=5):
        super().__init__(car_id=car_id, brand=brand, type='sedan')
        self.seats = seats
        self.day_charge = 100  # 默认日租金
        self.deposit = 1000  # 默认押金
    
    def __str__(self):
        return super().__str__() + f"\n座位数: {self.seats}"

class Bus(Car):
    __tablename__ = 'buses'
    
    id = Column(Integer, db.ForeignKey('cars.id'), primary_key=True)
    bus_loads = Column(Integer)  # 载客量
    
    __mapper_args__ = {
        'polymorphic_identity': 'bus',
    }
    
    def __init__(self, car_id, brand, bus_loads):
        super().__init__(car_id=car_id, brand=brand, type='bus')
        self.bus_loads = bus_loads
        self.day_charge = 300  # 默认日租金
        self.deposit = 2000  # 默认押金
    
    def __str__(self):
        return super().__str__() + f"\n载客量: {self.bus_loads}人"

class Truck(Car):
    __tablename__ = 'trucks'
    
    id = Column(Integer, db.ForeignKey('cars.id'), primary_key=True)
    volume = Column(Float)  # 载货体积(m³)
    capacity = Column(Float)  # 载货重量(吨)
    length = Column(Float)  # 长(m)
    width = Column(Float)  # 宽(m)
    height = Column(Float)  # 高(m)
    
    __mapper_args__ = {
        'polymorphic_identity': 'truck',
    }
    
    def __init__(self, car_id, brand, volume, capacity, length, width, height):
        super().__init__(car_id=car_id, brand=brand, type='truck')
        self.volume = volume
        self.capacity = capacity
        self.length = length
        self.width = width
        self.height = height
        self.day_charge = 200  # 默认日租金
        self.deposit = 1500  # 默认押金
    
    def __str__(self):
        return super().__str__() + (
            f"\n载货体积: {self.volume}m³"
            f"\n载货重量: {self.capacity}吨"
            f"\n尺寸(长×宽×高): {self.length}m × {self.width}m × {self.height}m"
        )

# 租车管理类
class CarRentalManager:
    @staticmethod
    def add_car():
        print("\n添加车辆")
        while True:
            car_type = input("车辆类型 (1-轿车, 2-巴士, 3-货车, 0-取消): ")
            if car_type == '0':
                return
            if car_type in ('1', '2', '3'):
                break
            print("错误: 无效的车辆类型，请重新输入")
        
        try:
            car_id = get_valid_input("车牌号: ", validate_car_id)
            brand = get_valid_input("品牌: ", str)
            
            if car_type == '1':
                seats = get_valid_input("座位数(默认5): ", validate_integer, default=5)
                car = Sedan(car_id, brand, seats)
            elif car_type == '2':
                bus_loads = get_valid_input("载客量: ", validate_integer)
                car = Bus(car_id, brand, bus_loads)
            elif car_type == '3':
                volume = get_valid_input("载货体积(m³): ", validate_positive_number)
                capacity = get_valid_input("载货重量(吨): ", validate_positive_number)
                length = get_valid_input("长度(m): ", validate_positive_number)
                width = get_valid_input("宽度(m): ", validate_positive_number)
                height = get_valid_input("高度(m): ", validate_positive_number)
                car = Truck(car_id, brand, volume, capacity, length, width, height)
            
            # 检查车牌号是否已存在
            if session.query(Car).filter_by(car_id=car_id).first():
                print("错误: 该车牌号已存在")
                return
            
            session.add(car)
            session.commit()
            print("车辆添加成功!")
        except Exception as e:
            session.rollback()
            print(f"添加车辆失败: {e}")

    @staticmethod
    def show_all_cars():
        print("\n所有车辆信息:")
        cars = session.query(Car).all()
        if not cars:
            print("当前没有车辆信息")
            return
        
        for car in cars:
            print(car)
            print("-" * 30)

    @staticmethod
    def query_car():
        car_id = input("\n请输入要查询的车牌号(留空查看所有): ").strip()
        if not car_id:
            CarRentalManager.show_all_cars()
            return
        
        car = session.query(Car).filter_by(car_id=car_id).first()
        if car:
            print(car)
        else:
            print("未找到该车辆!")

    @staticmethod
    def modify_car():
        car_id = input("\n请输入要修改的车牌号: ").strip()
        car = session.query(Car).filter_by(car_id=car_id).first()
        if not car:
            print("未找到该车辆!")
            return
        
        print("当前车辆信息:")
        print(car)
        
        print("\n修改选项:")
        print("1. 修改日租金")
        print("2. 修改押金")
        print("3. 修改品牌")
        print("0. 取消")
        
        while True:
            choice = input("请选择修改项: ").strip()
            if choice == '0':
                return
            if choice in ('1', '2', '3'):
                break
            print("无效选择!")
        
        try:
            if choice == '1':
                new_charge = get_valid_input("新的日租金: ", validate_positive_number)
                car.day_charge = new_charge
            elif choice == '2':
                new_deposit = get_valid_input("新的押金: ", validate_positive_number)
                car.deposit = new_deposit
            elif choice == '3':
                new_brand = get_valid_input("新的品牌: ", str)
                car.brand = new_brand
            
            session.commit()
            print("修改成功!")
        except Exception as e:
            session.rollback()
            print(f"修改失败: {e}")

    @staticmethod
    def delete_car():
        car_id = input("\n请输入要删除的车牌号: ").strip()
        if not car_id:
            print("车牌号不能为空")
            return
        
        car = session.query(Car).filter_by(car_id=car_id).first()
        if not car:
            print("未找到该车辆!")
            return
        
        if car.rented:
            print("错误: 该车辆正在租借中，不能删除")
            return
        
        confirm = input(f"确定要删除车牌号为 {car_id} 的车辆吗?(y/n): ").strip().lower()
        if confirm == 'y':
            try:
                session.delete(car)
                session.commit()
                print("车辆删除成功!")
            except Exception as e:
                session.rollback()
                print(f"删除失败: {e}")
        else:
            print("取消删除操作")

# 用户租车类
class CarRentalUser:
    @staticmethod
    def rent_car():
        print("\n可租借车辆:")
        available_cars = session.query(Car).filter_by(rented=False).all()
        if not available_cars:
            print("当前没有可租借的车辆!")
            return
        
        for idx, car in enumerate(available_cars, 1):
            print(f"{idx}. 车牌号: {car.car_id}, 类型: {car.type}, 品牌: {car.brand}, 日租金: {car.day_charge}元")
        
        while True:
            choice = input("\n请选择要租借的车辆编号(0-取消): ").strip()
            if choice == '0':
                return
            if choice.isdigit() and 1 <= int(choice) <= len(available_cars):
                car = available_cars[int(choice)-1]
                break
            print("无效选择!")
        
        try:
            renter = get_valid_input("租借人姓名: ", str)
            contact = get_valid_input("联系方式: ", validate_contact)
            rent_date = datetime.now().date()
            
            car.rented = True
            car.renter = renter
            car.renter_contact = contact
            car.date_rent = rent_date
            car.date_return = None
            
            session.commit()
            print(f"\n租借成功!")
            print(f"车牌号: {car.car_id}")
            print(f"押金: {car.deposit}元")
            print(f"日租金: {car.day_charge}元")
        except Exception as e:
            session.rollback()
            print(f"租借失败: {e}")

    @staticmethod
    def return_car():
        # 显示当前租借中的车辆
        rented_cars = session.query(Car).filter_by(rented=True).all()
        if not rented_cars:
            print("当前没有租借中的车辆!")
            return
        
        print("\n租借中的车辆:")
        for idx, car in enumerate(rented_cars, 1):
            rent_days = (date.today() - car.date_rent).days
            if rent_days < 1:
                rent_days = 1
            print(f"{idx}. 车牌号: {car.car_id}, 租借人: {car.renter}, 已租天数: {rent_days}, 预估费用: {rent_days * car.day_charge}元")
        
        while True:
            choice = input("\n请选择要归还的车辆编号(0-取消): ").strip()
            if choice == '0':
                return
            if choice.isdigit() and 1 <= int(choice) <= len(rented_cars):
                car = rented_cars[int(choice)-1]
                break
            print("无效选择!")
        
        try:
            return_date = datetime.now().date()
            rent_days = (return_date - car.date_rent).days
            if rent_days < 1:
                rent_days = 1
            
            total_charge = rent_days * car.day_charge
            
            car.rented = False
            car.date_return = return_date
            
            session.commit()
            
            print("\n归还成功!")
            print(f"车牌号: {car.car_id}")
            print(f"租借天数: {rent_days}天")
            print(f"总费用: {total_charge}元")
            print(f"押金退还: {car.deposit}元")
        except Exception as e:
            session.rollback()
            print(f"归还失败: {e}")

# 主菜单
def main_menu():
    Base.metadata.create_all(engine)  # 创建数据库表
    
    while True:
        print("\n===== 租车管理系统 =====")
        print("1. 管理员登录")
        print("2. 用户登录")
        print("3. 退出系统")
        choice = input("请选择: ").strip()
        
        if choice == '1':
            admin_menu()
        elif choice == '2':
            user_menu()
        elif choice == '3':
            print("感谢使用，再见!")
            break
        else:
            print("无效选择，请重新输入!")

def admin_menu():
    while True:
        print("\n===== 管理员菜单 =====")
        print("1. 添加车辆")
        print("2. 显示所有车辆")
        print("3. 查询车辆")
        print("4. 修改车辆")
        print("5. 删除车辆")
        print("0. 返回主菜单")
        choice = input("请选择: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            CarRentalManager.add_car()
        elif choice == '2':
            CarRentalManager.show_all_cars()
        elif choice == '3':
            CarRentalManager.query_car()
        elif choice == '4':
            CarRentalManager.modify_car()
        elif choice == '5':
            CarRentalManager.delete_car()
        else:
            print("无效选择，请重新输入!")

def user_menu():
    while True:
        print("\n===== 用户菜单 =====")
        print("1. 查询车辆")
        print("2. 租借车辆")
        print("3. 归还车辆")
        print("0. 返回主菜单")
        choice = input("请选择: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            CarRentalManager.query_car()
        elif choice == '2':
            CarRentalUser.rent_car()
        elif choice == '3':
            CarRentalUser.return_car()
        else:
            print("无效选择，请重新输入!")

if __name__ == "__main__":
    main_menu()