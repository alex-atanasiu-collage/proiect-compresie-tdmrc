#include <stdio.h>
#include <stdlib.h>

void store_compressed() {
}

void store_tmp_uncompressed() {
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        printf("Use the focking program as i want\n");
        return -1;
    }

    if (argv[1] == 'c') {
        store_compressed();
    } else if (argv[1] == 'u') {
        store_tmp_uncompressed();
    } else {
        printf("We only have 2 focking possible operations\n");
    }


    return 0;
}
