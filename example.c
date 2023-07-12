#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int foo(int* arr, int threshold, int n) {
    int sum = 0;
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            sum += arr[i*n+j];
        }
    }
    if(sum > threshold) {
        sum += threshold;
        // printf(":o");
    }
    return sum;
}

int bar(int* arr, int threshold, int n) {
    int buff = 1;
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            if(arr[i*n+j] != 0)
                buff *= arr[i*n+j];
        }
    }
    if(buff > threshold) {
        buff -= threshold;
        // printf(":o");
    }
    return buff;
}


int main() {
    int n = 100;
    int* arr = malloc(n*n*sizeof(int));
    srand(time(NULL));
    int threshold = rand();



    while(1) {
        for(int i = 0; i < n; i++) {
            for(int j = 0; j < n; j++) {
                arr[i*n+j] = rand();
            }
        }
        int a = foo(arr, threshold, n);
        int b = bar(arr, threshold, n);
        printf("%d\n", a+b);
    }

}