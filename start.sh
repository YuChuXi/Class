#!/usr/bin/bash
ulimit -c unlimited

make
$PWD/main.bin