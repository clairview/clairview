#!/bin/bash
set -e
cd typescript
pnpm run build
cd ..

cd ..

rm -f clairvm/__tests__/__snapshots__/*.stdout.nodejs
rm -f clairvm/__tests__/__snapshots__/*.stdout.python

for file in clairvm/__tests__/*.hog; do
    echo "Testing $file"

    # from clairvm/__tests__/*.hog get clairvm/__tests__/__snapshots__/*
    basename="${file%.hog}"
    basename="${basename##*/}"
    basename="clairvm/__tests__/__snapshots__/$basename"

    ./bin/hoge $file $basename.hoge
    ./bin/hog --nodejs $basename.hoge > $basename.stdout.nodejs
    ./bin/hog --python $basename.hoge > $basename.stdout.python
    set +e
    diff $basename.stdout.nodejs $basename.stdout.python
    if [ $? -eq 0 ]; then
        mv $basename.stdout.nodejs $basename.stdout
        rm $basename.stdout.python
    else
        echo "Test failed"
    fi
    set -e
done
