A simple json -> pdf way of handling my job applications. Mainly for my personal benifit.

# build

## Internal development build
Create a docker image by executing 
```bash
# ./build-container.sh
```

## Release
A tar-ball can be created by executing 
```bash
# ./build-release.sh
```

# Generating a pdf

- Create the directory data/ and populate content according to data structure described in example-data/ 
- Generate a pdf to the output/ directory by executing
```bash
# ./run-container.sh
```
