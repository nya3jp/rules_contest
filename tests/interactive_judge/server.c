#include <stdio.h>

int main(int argc, char** argv) {
    FILE* fp = fopen(argv[1], "r");
    int a, b;
    fscanf(fp, "%d%d", &a, &b);
    fclose(fp);

    fprintf(stderr, "SERVER: init: a=%d, b=%d\n", a, b);

    for (;;) {
        char c;
        scanf(" %c", &c);
        if (c == 'q') {
            int x;
            scanf("%d", &x);
            fprintf(stderr, "SERVER: input: q %d\n", x);
            printf("%d\n", a * x + b);
            fprintf(stderr, "SERVER: output: %d\n", a * x + b);
            fflush(stdout);
        } else if (c == 'a') {
            int p, q;
            scanf("%d%d", &p, &q);
            fprintf(stderr, "SERVER: input: a %d %d\n", p, q);
            return p == a && q == b ? 0 : 1;
        } else {
            return 1;
        }
    }
}
