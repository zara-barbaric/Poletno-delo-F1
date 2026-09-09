#!/bin/bash
wils="lq1"
index=242

for C in $(seq 0 0.5 30); do
	if [[ -d "/scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/C_${C}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/C_${C}
	fi
    if [ "$C" = "0.0" ]; then
        C=0.01
    fi
/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
import model SMEFTsim_general_MwScheme_UFO
define p = g u d s u~ d~ s~
generate p p > c e+ e- NP==1 / h a z h1 z1 c~
output /scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/C_${C}     
launch
0
set param_card smeft ${index} ${C}         
EOF
done
