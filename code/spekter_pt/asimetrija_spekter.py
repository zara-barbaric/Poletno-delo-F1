# Izriše graf asimetrije med kvarkoma c in c~ v odvisnosti od gibalne količine 
# Podatke dobi iz spektra gibalne količine, pridobljenega s programom Madanalysis

import numpy as np
import matplotlib.pyplot as plt
import re

###ZA SPREMENITI:
#Pot do histos.saf datotek, ki jih generira Madanalysis
file_c = "/home/zara/Documents/ma5/C_eu/pp_cee/C_1.0/Output/SAF/_defaultset/MadAnalysis5job_0/Histograms/histos.saf"
file_anti_c = "/home/zara/Documents/ma5/C_eu/pp_c~ee/C_1.0/Output/SAF/_defaultset/MadAnalysis5job_0/Histograms/histos.saf"
#Pot do končne slike
fig_path = "/home/zara/Documents/graphs/asimetrija_SMEFT.png"

#Izgled grafa
plt.rcParams.update({
    "figure.figsize": (3, 2),
    "font.size": 10,
    "font.family": "serif",
    'text.usetex': True,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "legend.fontsize": 6,
    "lines.linewidth": 1,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

#Prebere podatke histogramu iz saf datoteke
def read_saf(filename):
    with open(filename, "r") as f:
        content = f.read()
    
    #Podatki o intervalih
    header = re.search(r'# nbins\s+xmin\s+xmax\s*\n\s*(\d+)\s+([\d.e+-]+)\s+([\d.e+-]+)', content) 
    
    nbins = int(header.group(1))
    xmin = float(header.group(2))
    xmax = float(header.group(3))

    bin_width = (xmax - xmin) / nbins
    bin_edges = np.linspace(xmin,xmax,nbins+1,endpoint=True)

    #Sredine intervalov (pomembno za risanje grafa na koncu)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    #Vrednosti na posameznih intervalih
    data = re.search(r'<Data>\s*(.*?)\s*</Data>', content, re.DOTALL)   #Poišče del datoteke, kjer so podatki o vrednostih na intervalih 
    data_lines = data.group(1).strip().split('\n')                    
    bin_values = []
    
    for line in data_lines:
        parts = line.strip().split()      
        bin_values.append(float(parts[0]))

    underflow = bin_values[0]
    overflow = bin_values[-1]
    main_bin_values = bin_values[1:-1]      #Vrednosti na intervalih brez underflow in overflow

    return {
        'nbins': nbins,
        'xmin': xmin,
        'xmax': xmax,
        'bin_width': bin_width,
        'bin_edges': bin_edges,
        'bin_centers': bin_centers,
        'bin_values': np.array(main_bin_values),
        'underflow': underflow if 'underflow' in locals() else 0,
        'overflow': overflow if 'overflow' in locals() else 0,
        'raw_values': np.array(bin_values),
    }

#Izračuna asimetrijo
def asymetry(file_c, file_anti_c):
    """
    Izračuna asimetrijo med kvarkoma c in c~ (samo znotraj enega modela.
    
    Parametri
    ---------
    file_c : pot do datoteke histos.saf s podatki za histogram, ki ga ustvari Madanalysis za proces s kvarkom c
    file_anti_c : pot do datoteke histos.saf s podatki za histogram, ki ga ustvari Madanalysis za proces s kvarkom c~
    """

    data_c = read_saf(file_c)
    data_anti_c = read_saf(file_anti_c)

    bin_centers_c = data_c["bin_centers"]
    bin_centers_anti_c = data_anti_c["bin_centers"]
    
    if not np.array_equal(bin_centers_c, bin_centers_anti_c):
        raise ValueError(f"Bins do not match")

    bin_width = data_c["bin_width"]

    bin_values_c = data_c["bin_values"]
    bin_values_anti_c = data_anti_c["bin_values"]

    sum_vals = bin_values_c + bin_values_anti_c
    diff_vals = bin_values_c - bin_values_anti_c
    with np.errstate(divide='ignore', invalid='ignore'):
        bin_values = np.where(sum_vals != 0, diff_vals / sum_vals, 0)
    
    return bin_centers_c, bin_width, bin_values

bin_centers, bin_width, bin_values = asymetry(file_c, file_anti_c)

plt.bar(bin_centers, bin_values, width=bin_width, color="#5954d8", edgecolor='black', linewidth=0.5)
plt.xlabel("$p_T$ [GeV]")
plt.ylabel(r"$\frac{\sigma_c - \sigma_{\bar{c}}}{\sigma_c + \sigma_{\bar{c}}}$")
plt.savefig(fig_path)
plt.show()