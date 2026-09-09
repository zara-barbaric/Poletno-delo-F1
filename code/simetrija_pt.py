import numpy as np
import matplotlib.pyplot as plt
import re

colors1 = plt.cm.Set2(np.linspace(0, 1, 8))
plt.rcParams.update({
    "figure.figsize": (6, 4),
    "font.size": 15,
    "font.family": "serif",
    'text.usetex': True,
    "axes.labelsize": 15,
    "axes.titlesize": 15,
    "legend.fontsize": 10,
    "lines.linewidth": 1.5,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

def read_saf(filename):
    with open(filename, "r") as f:
        content = f.read()
    
    #Osnvni podatki
    header = re.search(r'# nbins\s+xmin\s+xmax\s*\n\s*(\d+)\s+([\d.e+-]+)\s+([\d.e+-]+)', content)
    if not header:
        raise ValueError("No header found")
    nbins = int(header.group(1))
    xmin = float(header.group(2))
    xmax = float(header.group(3))

    bin_width = (xmax - xmin) / nbins
    bin_edges = [xmin + i * bin_width for i in range(nbins + 1)]
    
    # Extract data
    data = re.search(r'<Data>\s*(.*?)\s*</Data>', content, re.DOTALL)
    if not data:
        raise ValueError("No <Data> section found")
    data_lines = data.group(1).strip().split('\n')
    
    bin_values = []
    bin_errors = []
    
    for line in data_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            bin_values.append(float(parts[0]))
            bin_errors.append(float(parts[1]))
    
    if len(bin_values) >= nbins + 2:
        underflow = bin_values[0]
        overflow = bin_values[-1]
        main_bins = bin_values[1:-1]
        main_errors = bin_errors[1:-1]
    else:
        main_bins = bin_values
        main_errors = bin_errors
    
    return {
        'nbins': nbins,
        'xmin': xmin,
        'xmax': xmax,
        'bin_edges': np.array(bin_edges),
        'bin_values': np.array(main_bins),
        'bin_errors': np.array(main_errors),
        'underflow': underflow if 'underflow' in locals() else 0,
        'overflow': overflow if 'overflow' in locals() else 0,
        'raw_values': np.array(bin_values),
        'raw_errors': np.array(bin_errors)
    }

def simetrija_data(file1, file2, file3):
    data1 = read_saf(file1)
    data2 = read_saf(file2)
    data3 = read_saf(file3)

    bin_edges1 = data1["bin_edges"]
    bin_edges2 = data2["bin_edges"]
    bin_edges3 = data3["bin_edges"]
    
    if not np.array_equal(bin_edges1, bin_edges2):
        raise ValueError(f"Bins do not match")
    
    bin_values1 = data1["bin_values"]
    bin_values2 = data2["bin_values"]
    bin_values3 = data3["bin_values"]

    sigma1 = bin_values1 + bin_values3
    sigma2 = bin_values2 + bin_values3

    sum_vals = sigma1 + sigma2
    diff_vals = sigma1 - sigma2
    
    with np.errstate(divide='ignore', invalid='ignore'):
        sym_values = np.where(sum_vals != 0, diff_vals / sum_vals, 0)
    
    
    return bin_edges1, sym_values

for i, Wils in enumerate(["eu", "lu", "qe", "lq1", "lq3", "lequ1", "lequ3"]):

    file1 = rf"/home/zara/Documents/ma5/C_{Wils}/pp_cee/meja/Output/SAF/_cee/MadAnalysis5job_0/Histograms/histos.saf"
    file2 = rf"/home/zara/Documents/ma5/C_{Wils}/pp_c~ee/meja/Output/SAF/_cee/MadAnalysis5job_0/Histograms/histos.saf"
    file3 = rf"/home/zara/Documents/ma5/SM/meja/Output/SAF/_cee/MadAnalysis5job_0/Histograms/histos.saf"

    if "1" in Wils:
        label = rf"$C_{{{Wils[:-1]}}}^{{(1)}}$"
    elif "3" in Wils:
        label = rf"$C_{{{Wils[:-1]}}}^{{(3)}}$"
    else:
        label = rf"$C_{{{Wils}}}$"

    bin_edges, sym_values = simetrija_data(file1, file2, file3)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Bars automatically fill from 0 to the value
    plt.plot(bin_centers, sym_values, color=colors1[i],linewidth=0.75, label=label)

plt.ylabel(r"$\frac{\sigma_c - \sigma_{\bar{c}}}{\sigma_c + \sigma_{\bar{c}}}$")
plt.xlabel("$p_T$ [GeV]")
plt.yscale("log", base=10)
plt.legend()
plt.savefig("/home/zara/Documents/graphs/graf_pt2.png")
plt.show()