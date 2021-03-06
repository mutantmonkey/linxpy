# linxpy

*Note: This software has been superseded by [golinx](https://github.com/mutantmonkey/golinx) and is here for historical purposes only. Do not expect it to work.*

A Python client for [linx.li](https://linx.li).

## Installation
1. `git clone https://github.com/mutantmonkey/linxpy.git`
2. `cd linxpy`
3. `python setup.py install`

## Usage

### Uploading Files
Upload hello.jpg:
```
linx hello.jpg
```

Upload hello.jpg, with an expiration time of 1 hour (3600 seconds):
```
linx -e 3600 hello.jpg
```

Upload hello.jpg, test.webm, and 20150401130001_AUD.flac:
```
linx hello.jpg test.webm 20150401130001_AUD.flac
```

### Uploading from stdin
You can also upload from standard input:
```
echo "Hello world" | linx
```

### Deleting Files
After files are uploaded, they can be deleted with the unlinx command:
```
unlinx https://linx.li/4vlx21i31.txt
```

This works because delete keys are automatically stored in
~/.local/share/linx.log as files are uploaded.
