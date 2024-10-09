#!/usr/bin/bash
ulimit -c unlimited
echo core > /proc/sys/kernel/core_pattern
make
$PWD/main.bin