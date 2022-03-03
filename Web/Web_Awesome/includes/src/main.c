#include <stdio.h>
#include <string.h>
#include <emscripten/emscripten.h>

EMSCRIPTEN_KEEPALIVE
int right_or_wrong(char a[])
{
    int i;
    char final_output[strlen(a)];
    for (i = 0; i < strlen(a); i++)
    {
        char temp = a[i] ^ 9;
        final_output[i] = temp;
    }
    final_output[i] = '\0';
    if (strcmp(final_output, "yVj}or;8|l~lcjkf0n{xmm0k:{1{>n~f`ma08n;:{|x:kt") == 0)
    {
        return 1;
    }
    return 0;
}