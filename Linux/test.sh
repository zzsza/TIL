#!/bin/sh

if [ -f file ]
then
    echo "file exists"
else
    echo "file not found"
fi

if [ -d file ]
then 
    echo "file is a directory"
else
    echo "file is not a directory"
fi

if [ -s file ]
then
    echo "file is not of zero length"
else
    echo "file size is zero length"
fi

if [ -r file -a -w file ]
then
    echo "file is readable and writable"
else
    echo "file is not read/write"
fi
