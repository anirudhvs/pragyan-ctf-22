#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>

char check_p1[] = ",QOH>EU'P";
char check_p2[] = ",S>DQ$S";
char check_p3[] = ",Q>AQ!S";

int set = 0;
char p1[12];
char p2[12];
char p3[12];

char* __encrypt(char inpString[],char* ptr)
{
    char xyz[] = "3T5*)Z'0B6";

    int len = strlen(inpString);
    char tmp[0];
    for (int i = 0; i < len; i++)
    {
        tmp[i] = inpString[i] ^ xyz[i];
    }
    strcpy(ptr, tmp);
    return ptr;
}
 

void tryOne(int param_1, int param_2, int param_3)

{
    sprintf(p1, "%p", param_1);
    sprintf(p2, "%p", param_2);
    sprintf(p3, "%p", param_3);

    char *dr;
    dr = (char *)malloc(10 * sizeof(char));

    if (((strcmp(p1, __encrypt(check_p1, dr)) != 0) || (strcmp(p2, __encrypt(check_p2, dr)) != 0)) || (strcmp(p3, __encrypt(check_p3, dr)) != 0))
    {
        exit(1);
    }
    puts("Nice Try");
    set = 1;
    free(dr);
    return;
}

void tryTwo(int param_1, int param_2, int param_3)

{
    sprintf(p1, "%p", param_1);
    sprintf(p2, "%p", param_2);
    sprintf(p3, "%p", param_3);

    char *dr;
    dr = (char *)malloc(10 * sizeof(char));
    // printf("%s",__encrypt(check_p2, fr));

    if (((strcmp(p1, __encrypt(check_p2, dr)) == 0) && (strcmp(p2, __encrypt(check_p3, dr)) == 0)) && (strcmp(p3, __encrypt(check_p1, dr)) == 0) && (set == 1))
    {
        set = 2;
        puts("Very Close");
        return;
    }
    free(dr);
    exit(1);
}

void tryThree(int param_1, int param_2, int param_3)

{
    sprintf(p1, "%p", param_1);
    sprintf(p2, "%p", param_2);
    sprintf(p3, "%p", param_3);

    char *dr = NULL;
    dr = (char *)malloc(10 * sizeof(char));

    if (((strcmp(p1, __encrypt(check_p3, dr)) == 0) && (strcmp(p2, __encrypt(check_p1, dr)) == 0)) && (strcmp(p3, __encrypt(check_p2, dr)) == 0) && (set == 2))
    {
        char *filename = "flag";
        FILE *fp = fopen(filename, "r");

        if (fp == NULL)
        {
            printf("Could not open %s", filename);
            exit(1);
        }

        const unsigned MAX_LENGTH = 256;
        char buffer[MAX_LENGTH];

        while (fgets(buffer, MAX_LENGTH, fp))
            printf("%s", buffer);

        fclose(fp);
        return;
    }
    free(dr);
    exit(1);
}