#!/bin/bash
DIR=`dirname $0`

case $2 in
n1) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/3.out $DIR/../../tests/blackbox/3.in && exit 0;;
n2) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/2.out $DIR/../../tests/blackbox/2.in && exit 0;;
n3) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/1.out $DIR/../../tests/blackbox/1.in && exit 0;;
n4) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/6.out $DIR/../../tests/blackbox/6.in && exit 0;;
n5) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/5.out $DIR/../../tests/blackbox/5.in && exit 0;;
n6) $DIR/../../../bin/genprog_tests.py --program checksum $1 $DIR/../../tests/blackbox/4.out $DIR/../../tests/blackbox/4.in && exit 0;;
esac
exit 1
