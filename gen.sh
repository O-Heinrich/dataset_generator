#!/bin/bash

if [ ! -d "generator_venv" ]; then
    echo "Did not find the virtual environment. Please use install.sh first."
    exit 1
fi

p=""
f=""
a=false
o=false
n=""
e=""
d=""
oneline=false
l=""
seed=""

print_usage() {
  printf "Usage:\nFlags:\n-p, -f, -a, -o, -n, -e, -d, -l: Same as for Script, see README\n-i: Equivalent to --oneline for Script, see README\n-s: Equivalent to --seed for Script, see README\n"
}

OPTIND=1
while getopts 'p:f:aon:e:d:il:' flag; do
  case $flag in
    p) p="${OPTARG}" ;;
    f) f="${OPTARG}" ;;
    a) a=true ;;
    o) o=true ;;
    n) n="${OPTARG}" ;;
    e) e="${OPTARG}" ;;
    d) d="${OPTARG}" ;;
    i) oneline=true ;;
    l) l="${OPTARG}" ;;
    s) seed="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

#if [ ! -z "$p" ]; then
#    shift $((OPTIND - 1))
#    p=$@
#fi

source ./generator_venv/bin/activate
command="python src/dataset_gen.py"
# Pass down given flags
if [ ! -z "$p" ]; then
    command="${command} -p ${p}"
fi
if [ ! -z "$f" ]; then
    command="$command -f $f"
fi
if $o; then
    command="$command -o"
elif $a; then
    command="$command -a"
fi
if [ ! -z "$n" ]; then
    command="$command -n $n"
fi
if [ ! -z "$e" ]; then
    command="$command -e $e"
fi
if [ ! -z "$d" ]; then
    command="$command -d $d"
fi
if $oneline; then
    command="$command --oneline"
fi
if [ ! -z "$l" ]; then
    command="$command -l $l"
fi
if [ ! -z "$seed" ]; then
    command="$command --seed $seed"
fi
eval $command
deactivate
exit 0
