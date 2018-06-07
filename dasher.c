#include <unistd.h>
int main() {
	while (!fork())
		;
}
