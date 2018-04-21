#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>


/*
 * Retrieves the content of @param filename which only contains 0s or 1s
 * Stores bitwise representation of the content in @param storagefile
 * @param storage file is the compressed format of the file
 *
*/
void store_compressed(const char *filename, const char *storagefile) {

    FILE *f = fopen(filename, "rb");
    FILE *g = fopen(storagefile, "wb");
    
    uint64_t file_size, padded_size, i, j, byte_index = 0;
    uint8_t *stream, *c_stream, bit_index = 0, padding_bits;

    if (f == NULL || g == NULL) {
        printf("Cannot open file or unknown formation\n");
        return;
    }

    fseek(f, 0, SEEK_END);
    file_size = ftell(f);
    fseek(f, 0, SEEK_SET);
    stream = malloc(file_size);
    fread(stream, sizeof(uint8_t), file_size, f);
    
    /*Number of 0s and 1s must be multiple of 8 so we padd with 0s at the end*/
    if ((file_size % 8) != 0)
         padded_size = file_size +  (8 - (file_size %8));
    else
         padded_size = file_size;

    padding_bits = padded_size - file_size;
    /*We also store the number of padding bits for reconversion*/
    fwrite(&padding_bits, sizeof(uint8_t), 1, g);
    c_stream = calloc(padded_size/8, sizeof(uint8_t));
    for (i = 0; i < file_size; i++) {
        if (i % 8 == 0 && i != 0) {
            byte_index++;
            bit_index = 0;
        }
        /*bitwise representation of chars*/
        /*same order as they are in the original file (this is why we have 7 - bit_index)*/
        if (stream[i] == '0')
            c_stream[byte_index] = c_stream[byte_index] & ~(1 << (7 - bit_index));
        else
            c_stream[byte_index] = c_stream[byte_index] | (1 << (7 -bit_index));

        bit_index++;
    }

    fwrite(c_stream, sizeof(uint8_t), byte_index + 1, g);
    free(c_stream);
    free(stream);

    /*
    Integrity check, decomment for debug
    uint64_t k = 0;
    for (i = 0; i < byte_index; i++) {
        for (j = 0; j < 8; j++) {
            if (stream[k] == '0' && ((c_stream[i] >> (7 - j)) & 0x01))
                printf("Err\n");
            if (stream[k] == '1' && !((c_stream[i] >> (7 - j)) & 0x01))
                printf("Err\n");
            k++;
        }
    }*/

    fclose(f);
}

/*
 * Converts the bitwise representation of compressed format @param storage_file
 * To a text representation of the bits @param tmp_file
 *
 *
*/
void store_tmp_uncompressed(const char *storage_file, const char *tmp_file) {

    FILE *f = fopen(storage_file, "rb");
    FILE *g = fopen(tmp_file, "wb");    
    uint8_t padding_bits, *c_stream, *stream, bit_index = 0;
    uint64_t file_size, stream_size, i, byte_index = 0;

    if (f == NULL || g == NULL) {
        printf("Cannot open file or unknown format");
        return;
    }

    fseek(f, 0, SEEK_END);
    file_size = ftell(f);
    fseek(f, 0, SEEK_SET);

    fread(&padding_bits, sizeof(uint8_t), 1, f);
    c_stream = malloc((file_size - 1) * sizeof(uint8_t));
    fread(c_stream, sizeof(uint8_t), file_size - 1, f);
    stream_size = (file_size - 1) * 8 * sizeof(uint8_t) - padding_bits;
    
    stream = malloc(stream_size * sizeof(uint8_t));
    for (i = 0; i < stream_size; i++) {
        if (i%8 == 0 && i != 0) {
            byte_index++;
            bit_index=0;
        }

        if ((c_stream[byte_index] >> (7 - bit_index)) & 0x01)
            stream[i] = '1';
        else
            stream[i] = '0';
        bit_index++;
    }

    fwrite(stream, sizeof(uint8_t), stream_size, g);

    fclose(f);
    fclose(g);
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        printf("Use the focking program as i want\n");
        return -1;
    }

    if (strcmp(argv[1], "u") == 0) {
        store_compressed(argv[2], argv[3]);
    } else if (strcmp(argv[1], "v") == 0) {
        store_tmp_uncompressed(argv[2], argv[3]);
    } else {
        printf("We only have 2 focking possible operations\n");
    }


    return 0;
}
