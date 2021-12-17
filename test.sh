#!/bin/bash
COUNTER=0
readarray -t depth < inputs/day_01.txt
len=$((${#depth[@]}+1))

for i in $(seq 0 ${len})
do
if [[ "${depth[$i]}" -lt "${depth[$i+1]}" ]]
then
        (( COUNTER++ )) || true
fi
done
printf '%s\n' "${COUNTER}"
