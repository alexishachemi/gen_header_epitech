# gen_header
### syncs header files with C files and creates new header files accordingly <br>
ignores "main" functions and "main.c" files by default <br>
can also merge all prototypes and includes in a single header file by specifying a file name (see -h for more info)<br>
**does not work with file names containing spaces**<br>
requires [cproto](https://invisible-island.net/cproto/cproto.html) to work