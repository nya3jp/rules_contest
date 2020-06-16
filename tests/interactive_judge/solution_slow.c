#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
    printf("q 0\n");
    fflush(stdout);
    int b;
    scanf("%d", &b);

    if (b == 4) {
        sleep(10);
    }

    printf("q 1\n");
    fflush(stdout);
    int ab;
    scanf("%d", &ab);

    int a = ab - b;
    printf("a %d %d\n", a, b);
    return 0;
}
