#include <stdio.h>

void sorted(int a[], int len)
{
    for (int i = len - 1; i >= 0; i--)
    {
        int c = 0;
        for (int j = 0; j < i; j++)
        {
            if (a[j] > a[j + 1])
            {
                int tmp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = tmp;
                c++;
            }
        }
        if (c == 0)
        {
            break;
        }
    }
}

int n = 0;
int rean(int i)
{
    n++;
    if (i == 1)
    {
        return i;
    }
    else
    {
        return rean(i - 1) + rean(i - 1);
    }
}

int main()
{
    int a[] = {1, 546, 4, 4, 5, 7, 34, 323, 12, 968, 8, 76, 5, 21};
    int len = sizeof(a) / sizeof(int);
    printf("%d\n", len);

    sorted(a, len);

    for (int i = 0; i < len; i++)
    {
        printf("-%d \n", a[i]);
    }

    printf("%d:%d", rean(31), n);
    return 0;
}
