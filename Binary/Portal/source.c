#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FLAG_BUFFER 128
#define PACK_SIZE 4

int check = 0;

int see_profile()
{
	printf("\nYour Profile: ");

	printf("\n\n");
	if (!check)
	{
		printf("You have base pack!\n");
	}
	else
	{
		printf("You have still have base pack :(\n");
		printf("Could not upgrade LOL. See available packs for you.\n\n");
		int money = (rand() % 2021) + 1;
		int value = 0;
		while (money > 0)
		{
			value = (rand() % money) + 1;
			char pack[PACK_SIZE + 1];
			int pack_len = (rand() % PACK_SIZE) + 1;
			for (int i = 0; i <= PACK_SIZE; i++)
			{
				if (i < pack_len)
				{
					pack[i] = 'A' + (rand() % 26);
				}
				else
				{
					pack[i] = '\0';
				}
			}
			money -= value;
			printf("%s pack worth of RS.%d\n", pack, value);
		}
	}
	return 0;
}

int upgrade_pack()
{
	char true_buf[FLAG_BUFFER];
	FILE *f = fopen("flag_maybe", "r");
	if (!f)
	{
		printf("Flag not found.\n");
		exit(1);
	}
	fgets(true_buf, FLAG_BUFFER, f);
	printf("Upgrading PAcK\n");

	char *val_buf = malloc(300 + 1);
	printf("Enter coupon code:\n");
	scanf("%300s", val_buf);
	printf("Upgrading pack with the coupon:\n");
	printf(val_buf);

	check = 1;
	see_profile();

	return 0;
}

int main(int argc, char *argv[])
{
	setbuf(stdout, NULL);
	int choice = 0;

	printf("Welcome!\n\n");
	printf("What would you like to do?\n");
	printf("1) Visit Profile\n");
	printf("2) Upgrade Pack\n");
	scanf("%d", &choice);

	if (choice == 1)
	{
		see_profile();
	}
	else if (choice == 2)
	{
		upgrade_pack();
	}

	printf("Bye!\n");

	exit(0);
}