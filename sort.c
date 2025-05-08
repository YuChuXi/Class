#include <stdio.h>
#include <stdlib.h>

int t(int a){
    return a;
}

int main(){
    int a[]={2,5,7,89,5,41,1,2,3,6,5,5,2};
    qsort(a, sizeof(a)/sizeof(int),t);
    for(int i=0;i<sizeof(a)/sizeof(int);i++){
        printf("%d ",a[i]);
    }

}