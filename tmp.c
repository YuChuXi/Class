#include <stdio.h>
void main()
{
    int n, s = 1;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++)
        s *= i;
    printf("%d\n", s);
}