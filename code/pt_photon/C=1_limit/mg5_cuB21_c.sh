#!/bin/bash
wils="uB21"
index=79
c=1

mkdir -p /scratch/barbariczara/2026/mg5/C_${wils}/pp_c~a/meja_limit/C_${c}

for pt in $(seq 5 5 500); do
	if [[ -d "/scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja_limit/C_${c}/pt_${pt}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja_limit/C_${c}/pt_${pt}
	fi
/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
import model SMEFTsim_general_MwScheme_UFO
generate p p > c a NP==1
output /scratch/barbariczara/2026/mg5/C_${wils}/pp_ca/meja_limit/C_${c}/pt_${pt}     
launch
0
set param_card smeft ${index} ${c}
set run_card ptj ${pt} 
set run_card ptamax 600     
EOF

done
