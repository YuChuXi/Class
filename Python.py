import os

with open("main.c", "w") as f:
    f.write(
        """#include <stdio.h>
int main()
{
   int a;
   scanf("%d", &a);
   switch (a)
   {
"""
        + (
            "".join(
                [
                    """   case %d:
      printf("星期%d");
      break;
"""
                    % (n, n)
                    for n in range(1000000)
                ]
            )
        )
        + """   default:
      break;
   }
   return 0;
}"""
    )
