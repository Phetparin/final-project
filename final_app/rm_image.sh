#!/bin/bash
#remove all docker images

for i in  $(sudo docker images | awk '($1 == "<none>") {print $3}')
do
    sudo docker rmi -f $i
done