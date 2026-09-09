#!/usr/bin/bash
#SBATCH --job-name=C_lequ1_cee
#SBATCH --partition=short
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --qos=student
#SBATCH --output=/home/barbariczara/2026/output/pt_electron/C_lequ1_cee.out

module load GCC/7.3.0
module load GCCcore/7.3.0

source /home/barbariczara/root/root_install/bin/thisroot.sh
source ~/.bashrc

#Commands:
bash ~/2026/code/pt_electron/mg5_clequ1_c.sh
