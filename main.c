#include <stdio.h>
int main()
{
   int x, y, q, c = 0;
   scanf("%d%d", &x, &y);
   float e = 3344.0;
   q=30;
   if (x>=5)
      q = 50;
   c = q *y;

   if (y>40){
      c = c+(y-40)*q/2;

   }

   printf("%d", c);
   return 0;
}

// 13 2 34
// 10 + 10*2 + 0