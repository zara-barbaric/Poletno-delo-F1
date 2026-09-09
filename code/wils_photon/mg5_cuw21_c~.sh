#!/bin/bash
wils=uW21
index=70

for C in $(seq 0 0.5 20); do
    if [[ -d "/scratch/barbariczara/2026/mg5/C_${wils}/pp_c~a/C_${C}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/C_${wils}/pp_c~a/C_${C}
	fi
    if [ "$C" = "0.0" ]; then
        C=0.01
    fi

/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
import model SMEFTsim_general_MwScheme_UFO
generate p p > c~ a NP==1
output /scratch/barbariczara/2026/mg5/C_{wils}/pp_c~a/C_${C}     
launch
0
set run_card ptamax 40
set param_card smeft ${index} ${C}          
EOF

done
