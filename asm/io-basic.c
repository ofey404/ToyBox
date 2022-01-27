#include <stdio.h>

int main() {
  int a = 10, b = 0;
  printf("b = %d\n", b);
  __asm__(
      "movl %1, %%eax;\n"
      "movl %%eax, %0;"
      : "=r"(b) /* output */
      : "r"(a)  /* input */
      : "%eax"  /* clobbered register */
  );
  printf("Execute some asm\n");
  printf("b = %d\n", b);
}
