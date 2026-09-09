#!/bin/bash
wils="uW21"
index=70
C=1

mkdir -p /scratch/barbariczara/2026/mg5/C_${wils}/pp_c~a/meja/C_${C}

for pt in $(seq 20 5 500); do
	if [[ -d "/scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja/C_${C}/pt_${pt}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja/C_${C}/pt_${pt}
	fi
/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
import model SMEFTsim_general_MwScheme_UFO
generate p p > c a NP==1
output /scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja/C_${C}/pt_${pt}     
launch
0
set param_card smeft ${index} ${C}
set run_card ptj ${pt}      
EOF

done
