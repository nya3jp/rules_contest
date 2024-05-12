#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
    int n;
    scanf("%d", &n);
    if (n >= 2) {
        sleep(60);
    }
    printf("%d\n", n * 42);
    return 0;
}
