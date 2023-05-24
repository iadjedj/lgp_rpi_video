#include <stdio.h>
#include <linux/ioctl.h>
#include <linux/fb.h>

int main(int argc, char **argv)
{
	printf("Value is: %d\n", FBIO_WAITFORVSYNC);
	return 0;
}
