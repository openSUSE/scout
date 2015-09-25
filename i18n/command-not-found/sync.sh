#/bin/bash

FILE=$(basename $1)

cp $1 ${FILE#command-not-found.} 
