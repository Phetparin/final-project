#!/bin/bash
#remove all container 

for i in $(sudo docker container ps -a | awk '{print $NF}')
do
  sudo docker container rm -f $i
done


