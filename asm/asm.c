#include <stdio.h>

int main() {
    int i = 1;
    i = i + 2;
    __asm__ ("addl	$2, -4(%rbp)");
    printf("%d\n", i);
}
