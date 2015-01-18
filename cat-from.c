#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


void validate_args_or_die(int argc, char **argv, long *offset_p, char **path_p);
void print_usage_and_exit(char *error_message);
void fatal_error(char *error_message);


int main(int argc, char **argv) {

    if (sizeof(long) != 8) {
        fatal_error("expected sizeof(long) to be 8 -- we want fseek(-, long, -) to be safe");
    }

    long offset;
    char *path;
    validate_args_or_die(argc, argv, &offset, &path);

    FILE *file = fopen(path, "r");
    if (!file) {
        fatal_error("we failed to open the file");
    }

    if (fseek(file, offset, SEEK_SET) != 0) {
        fatal_error("we failed to seek to that offset in the file");
    }

    long total_bytes_read = 0;

    // If you change kBufferSize, update the "larger-than-buffer" test
    const int kBufferSize = 32000;
    char buffer[kBufferSize];
    while (1) {
        long num_bytes_read = fread(buffer, 1, kBufferSize, file);
        if (num_bytes_read == 0) {

            if (feof(file) == 0) {
                fatal_error("fread failed");
            }

            if (total_bytes_read == 0) {
                fseek(file, 0, SEEK_END);
                long file_size = ftell(file);
                if (offset > file_size) {
                    fatal_error("the offset is larger than the file");
                }
            }

            return 0; 
        }
        if (fwrite(buffer, num_bytes_read, 1, stdout) != 1) {
            fatal_error("writing to stdout failed");
        }
    }

}


void validate_args_or_die(int argc, char **argv, long *offset_p, char **path_p) {

    if (argc != 4) {
        print_usage_and_exit("exactly three args required");
    }

    const char *offset_label_string = argv[1];
    const char *offset_string = argv[2];
    const char *path = argv[3];

    if (strcmp(offset_label_string, "--offset") != 0) {
        print_usage_and_exit("the first arg must be \"--offset\"");
    }

    long offset_string_length = strlen(offset_string);
    if (offset_string_length == 0) {
        print_usage_and_exit("the offset arg must contain digits");
    }
    if (offset_string_length > 18) {
        print_usage_and_exit("the offset arg must contain at most 18 digits");
        // because 19 digits could exceed a signed 64-bit integer
    }
    for (long i = 0; i < strlen(offset_string); i++) {
        if (!isdigit(offset_string[i])) {
            print_usage_and_exit("the offset arg must only contain digits");
        }
    }

    *offset_p = atol(argv[2]);
    *path_p = argv[3];
}


void print_usage_and_exit(char *error_message) {
    fprintf(stderr, "\n" \
                    "Error: %s\n" \
                    "\n" \
                    "Usage:  cat-from --offset N <file>\n" \
                    "\n", error_message);
    exit(1);
}


void fatal_error(char *error_message) {
    fprintf(stderr, "Error: %s\n", error_message);
    exit(1);
}
