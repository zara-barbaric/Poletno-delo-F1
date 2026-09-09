#!/bin/bash

for pt in $(seq 20 5 300); do
	if [[ -d "/scratch/barbariczara/2026/mg5/SM/meja/pt_${pt}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/SM/meja/pt_${pt}
	fi
/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
generate p p > c e+ e-
output /scratch/barbariczara/2026/mg5/SM/meja/pt_${pt}     
launch
0 
set run_card ptj ${pt}      
EOF

done
