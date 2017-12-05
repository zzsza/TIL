#!/bin/sh

number=0
while [ "$number" -lt 10 ]
do
echo "$number"
number='expr $number + 1'
done
echo "script complete"
