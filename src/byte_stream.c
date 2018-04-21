#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void store_compressed(const char *filename) {

    FILE *f = fopen(filename, "rt");
    fclose(f);
}

void store_tmp_uncompressed() {
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        printf("Use the focking program as i want\n");
        return -1;
    }

    if (strcmp(argv[1], "u") == 0) {
        store_compressed(argv[2]);
    } else if (strcmp(argv[1], "v") == 0) {
        store_tmp_uncompressed();
    } else {
        printf("We only have 2 focking possible operations\n");
    }


    return 0;
}
