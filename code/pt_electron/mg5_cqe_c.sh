#!/bin/bash
wils="qe"
index=727

for pt in $(seq 20 5 500); do
	if [[ -d "/scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/meja/pt_${pt}" ]]; then
		rm -r /scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/meja/pt_${pt}
	fi
/home/barbariczara/python3/bin/python3.7 /home/barbariczara/tools/mg5_amc/bin/mg5_aMC <<EOF
import model SMEFTsim_general_MwScheme_UFO
define p = g u d s u~ d~ s~
generate p p > c e+ e- NP==1 / h a z h1 z1 c~
output /scratch/barbariczara/2026/mg5/C_${wils}/pp_cee/meja/pt_${pt}     
launch
0
set param_card smeft ${index} 0.0423928
set run_card ptj ${pt}         
EOF

done
