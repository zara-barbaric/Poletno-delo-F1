#!/bin/bash

/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
generate p p > c~ e+ e-
output /scratch/barbariczara/2026/mg5/SM/wils_electron     
launch
0      
EOF
