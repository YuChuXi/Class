#include <stdio.h>

#define TOTAL_DISKS 14

int A[TOTAL_DISKS];
int B[TOTAL_DISKS];
int C[TOTAL_DISKS];

void printDisk(int diskNum)
{
    for (int i = 0; i < TOTAL_DISKS; i++)
    {
        printf((TOTAL_DISKS - i <= diskNum) ? "@" : " ");
    }
    printf("|");
    for (int i = 0; i < TOTAL_DISKS; i++)
    {
        printf((i < diskNum) ? "@" : " ");
    }
    printf(" ");
}

void printTowers()
{
    for (int i = TOTAL_DISKS - 1; i >= 0; i--)
    {
        printDisk(A[i]);
        printDisk(B[i]);
        printDisk(C[i]);
        printf("\n");
    }

    char *a[] = {"A", "B", "C"};
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < TOTAL_DISKS; j++)
        {
            printf("=");
        }
        printf(a[i]);
        for (int j = 0; j < TOTAL_DISKS; j++)
        {
            printf("=");
        }
        printf(" ");
    }
    printf("\n");
}

void moveOneDisk(int startTower[], int endTower[])
{
    int disk;
    for (int i = TOTAL_DISKS - 1; i >= 0; i--)
    {
        if (startTower[i] != 0)
        {
            disk = startTower[i];
            startTower[i] = 0;
            break;
        }
    }
    for (int i = 0; i < TOTAL_DISKS; i++)
    {
        if (endTower[i] == 0)
        {
            endTower[i] = disk;
            break;
        }
    }
}

void solve(int numberOfDisks, int startTower[], int tempTower[], int endTower[])
{
    // 递归解决汉诺塔问题
    if (numberOfDisks > 0)
    {
        solve(numberOfDisks - 1, startTower, endTower, tempTower);
        moveOneDisk(startTower, endTower);
        printTowers();
        solve(numberOfDisks - 1, tempTower, startTower, endTower);
    }
}

int main()
{
    // 初始化塔
    int i = 0;
    for (i = 0; i < TOTAL_DISKS; i++)
    {
        A[i] = TOTAL_DISKS - i;
    }
    for (i = 0; i < TOTAL_DISKS; i++)
    {
        B[i] = 0;
    }
    for (i = 0; i < TOTAL_DISKS; i++)
    {
        C[i] = 0;
    }

    printTowers(); // 打印初始状态
    solve(TOTAL_DISKS, A, B, C); // 解决汉诺塔问题
    return 0;
}