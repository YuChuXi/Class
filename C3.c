#include <stdio.h>

int main(){
    unsigned char *a = "g5resgrhsehyrjt5438729vhsrz";
    while(1 || *a != 0){
        printf("%02x ", *a);
        a=a+1;
    }

}