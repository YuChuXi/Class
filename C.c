#include <stdio.h>

int main() {
    int n, i, j;
    // 读取输入的整数n
    scanf("%d", &n);
    
    // 循环打印平行四边形的每一行
    for (i = 0; i < n; i++) {
        // 打印前导空格，除了最后一行
        if (i != n - 1) {
            for (j = 0; j < n - i - 1; j++) {
                printf(" ");
            }
        }
        // 打印星号和空格
        for (j = 0; j < n; j++) {
            if (i == 0 || i == n - 1 || j == 0 || j == n - 1) {
                printf("*");
            } else {
                printf(" ");
            }
        }
        // 换行
        printf("\n");
    }
    
    return 0;
}