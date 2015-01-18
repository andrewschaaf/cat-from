**cat a file after seeking to a specified byte offset**

[![Build Status](https://secure.travis-ci.org/andrewschaaf/cat-from.png)](https://travis-ci.org/andrewschaaf/cat-from)

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
