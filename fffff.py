import cv2
import torch
import numpy as np

# 配置参数
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
POPULATION_SIZE = 20  # 种群大小
GENERATIONS = 1000    # 迭代次数
PATCH_SIZE = 8        # 分块尺寸
MUTATION_RATE = 0.1   # 变异概率
ELITE_SIZE = 2        # 精英保留数量
TOURNAMENT_SIZE = 3   # 锦标赛选择规模

def main():
    # 读取目标图片
    target = cv2.imread("/home/yuchuxi/Pictures/2016-11-29-874845.png")[:, :, ::-1]  # 转换为RGB
    target = target.astype(np.float32) / 255.0
    h, w, c = target.shape
    
    # 转换为PyTorch张量
    target_tensor = torch.tensor(target, device=DEVICE).permute(2, 0, 1).unsqueeze(0)
    
    # 初始化随机种群
    population = torch.rand((POPULATION_SIZE, c, h, w), device=DEVICE)
    
    # 创建可视化窗口
    cv2.namedWindow("Evolution Progress", cv2.WINDOW_NORMAL)
    
    for generation in range(GENERATIONS):
        # 计算适应度（MSE）
        fitness = torch.mean((population - target_tensor)**2, dim=(1,2,3))
        
        # 选择精英
        _, elite_indices = torch.topk(-fitness, ELITE_SIZE)
        elites = population[elite_indices]
        
        # 可视化当前最佳个体
        best_idx = elite_indices[0]
        best_img = population[best_idx].permute(1, 2, 0).cpu().numpy()
        display_img = (best_img * 255).astype(np.uint8)[:, :, ::-1]  # 转回BGR格式
        
        # 添加信息文字
        # 修改后的可视化部分
        best_img = population[best_idx].permute(1, 2, 0).contiguous().cpu().numpy()  # 添加contiguous()
        display_img = (best_img * 255).astype(np.uint8)[:, :, ::-1]  # 转回BGR格式
        display_img = np.ascontiguousarray(display_img)  # 确保内存连续

        # 添加信息文字
        text = f"Gen: {generation}  MSE: {fitness[best_idx]:.5f}"
        cv2.putText(display_img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Evolution Progress", display_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        # 锦标赛选择
        selected = []
        for _ in range(POPULATION_SIZE - ELITE_SIZE):
            candidates = torch.randint(POPULATION_SIZE, (TOURNAMENT_SIZE,))
            winner = candidates[torch.argmin(fitness[candidates])]
            selected.append(population[winner])
        selected = torch.stack(selected)
        
        children = []
        for i in range(0, len(selected), 2):
            if i+1 >= len(selected):
                break
            
            # 分块处理 (添加维度说明)
            p1 = selected[i].unfold(1, PATCH_SIZE, PATCH_SIZE)  # [C, H_patches, W, PS]
            p1 = p1.unfold(2, PATCH_SIZE, PATCH_SIZE)           # [C, H_patches, W_patches, PS, PS]
            p2 = selected[i+1].unfold(1, PATCH_SIZE, PATCH_SIZE).unfold(2, PATCH_SIZE, PATCH_SIZE)
            
            # 创建交叉掩码 (保持维度对齐)
            mask = torch.rand(p1.shape[1:3], device=DEVICE) < 0.5  # [H_patches, W_patches]
            mask = mask.unsqueeze(0).unsqueeze(-1).unsqueeze(-1)   # [1, H_patches, W_patches, 1, 1]
            
            # 执行交叉并重组维度
            child = torch.where(mask, p1, p2)
            
            # 正确重组维度步骤
            # 1. 合并分块维度 [C, H_patches, W_patches, PS, PS]
            # 2. 置换维度为 [C, H_patches, PS, W_patches, PS]
            # 3. 合并成最终形状 [C, H, W]
            child = child.permute(0, 1, 3, 2, 4).contiguous()  # 交换W_patches和PS位置
            # 计算实际分块数量和元素总数
            h_patches = (h + PATCH_SIZE - 1) // PATCH_SIZE
            w_patches = (w + PATCH_SIZE - 1) // PATCH_SIZE
            total_elements = child.size(0) * h_patches * PATCH_SIZE * w_patches * PATCH_SIZE
            # 安全重组维度
            child = child.reshape(total_elements // (h * w), h, w)
            
            children.append(child)
        
        # 变异操作
        for i in range(len(children)):
            if torch.rand(1) < MUTATION_RATE:
                noise = torch.randn_like(children[i]) * 0.1
                children[i] = torch.clamp(children[i] + noise, 0, 1)
        
        # 生成新一代种群
        children = torch.stack(children[:POPULATION_SIZE - ELITE_SIZE])
        # 确保所有张量尺寸一致
        assert elites.shape[1:] == children.shape[1:], f"尺寸不匹配: {elites.shape} vs {children.shape}"
        population = torch.cat([elites, children])
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
