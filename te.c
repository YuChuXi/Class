#include <stdio.h>
int main()
{
    int n, m = 0, s;
    scanf("%d", &n);
    for (int i = 2; i <= n; i++)
    {
        s = 0;
        for (int j = 0; j <= i / 2; j++)
            if (i % j == 0)
                s += j;
        if (s == i)
        {
            printf("%d ", i);
            m++;
        }
    }
    if (m == 0)
        printf("NO");
    return 0;
}