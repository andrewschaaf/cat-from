**cat a file after seeking to a specified byte offset**

[TODO: Travis badge]

    cat-from --offset 123 foo | ...


### Pseudocode

    file = fopen(...)
    
    fseek(...offset...)
    
    until done:
      fread(...file...)
      fwrite(...stdout...)
    
    fclose(file)


### Design goals

- Validate arguments with care
- Detect and handle any {fopen,fseek,fread,fwrite,fclose} errors
- Minimize latency (launch time, etc)
- Maximize throughput


### [License: MIT](LICENSE.txt)
