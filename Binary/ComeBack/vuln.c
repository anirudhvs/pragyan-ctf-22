#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>

void sysfuncs(void)

{
  tryThree(4, 5, 6);
  tryTwo(4, 5, 6);
  tryOne(4, 5, 6);
}

void new_main(void)

{
  char inp[40];

  memset(inp, 0, 0x20);
  puts("All the Best :)\n");
  read(0, inp, 0x200);
  puts("Thank you!");
  return;
}

int main()

{
  setvbuf(stdout,(char *)0x0,2,0);
  new_main();
  puts("\nBYE");
  return 0;
}