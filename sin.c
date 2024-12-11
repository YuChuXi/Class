#include <stdio.h>
#include <math.h>
#define EPS 1E-5F
#define PI acos(-1)

double L_sin(double x)
{
    //x = fmod(x, PI * 2);
    double sum = 0.0;
    double term;
    double x_squared = x * x;
    double sign = -1.0;
    double factorial = 1.0;
    int n = 1;

    do
    {
        sum += (term = (sign = -sign) * x / factorial);
        x *= x_squared;
        factorial *= ((n + 2) * (n + 1));
        n += 2;
    } while (fabs(term) >= EPS);

    return sum;
}

int main()
{
    double x;
    scanf("%lf", &x);
    double L_y = L_sin(x);
    double std_y = sin(x);
    printf("L_y = %.30lf\n", L_y);
    printf("std_y = %.30lf\n", std_y);
    printf("loss = %.30lf\n", fabs(L_y - std_y));

    return 0;
}