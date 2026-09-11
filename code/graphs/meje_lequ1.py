import numpy as np
import matplotlib.pyplot as plt
import os
import re
import glob

###ZA SPREMENITI:
#Pot do mape s celotnim projektom
main = "/scratch/barbariczara/2026"
#Pot do končne slike 
fig_path = f"{main}/graphs/meje_lequ1.png"

#Izgled grafa
colors1 = plt.cm.Set2(np.linspace(0, 1, 8))
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

meje = {
    "eu": 0.0539771,
    "lu": 0.0540114,
    "qe": 0.0423928,
    "lq1": 0.0503483,
    "lq3": 0.0265658,
    "lequ1": 0.0562678,
    "lequ3": 0.0270081
}

def sigma(filename):
    """
    Poišče datoteko z rezultati programa Madgraph in vrne sipalni presek (prvo število).
    """

    try:
        with open(filename, "r") as f:
            line = f.readline()
        results = line.split()
        sigma = float(results[0])
        return sigma

    except FileNotFoundError:
        print(f"FILE NOT FOUND: {filename}")
        return None

def asymetry(file_sm, file_c, file_anti_c, c):
    """ 
    Izračuna asimetrijo med kvarkoma c in c~.
    
    Parametri
    ----------
    file_sm : pot do datoteke results.dat s sipalnim presekom, ki jo ustvari Madgraph za proces v standardnem modelu
    file_c : pot do datoteke results.dat s sipalnim presekom, ki jo ustvari Madgraph za proces s kvarkom c v SMEFT
    file_c : pot do datoteke results.dat s sipalnim presekom, ki jo ustvari Madgraph za proces s kvarkom c~ v SMEFT
    c : vrednosti Wilsonovega koeficienta, ki je bil nastavljen pri generaciji dogodkov
    """

    sigma_sm = sigma(file_sm)
    sigma_c = sigma(file_c)
    sigma_anti_c = sigma(file_anti_c)

    if sigma_sm is None or sigma_c is None or sigma_anti_c is None:
        return None

    combined_sigma_c = sigma_sm + c**2 * sigma_c
    combined_sigma_anti_c = sigma_sm + c**2 * sigma_anti_c

    c_sum = combined_sigma_c + combined_sigma_anti_c
    c_diff = combined_sigma_c - combined_sigma_anti_c

    if c_sum == 0:
        print(f"ZERO SUM OF CROSS SECTIONS: {file_c}")
        return None

    return c_diff / c_sum




#Za Wilsonov koeficient C_lequ1 izračuna asimetrijo in nariše graf
Wils = "lequ1"

#Poišče mape oblike C_*, kjer je * vrednost Wilsonovega koeficienta. To so mape, ki jih določimo kot output v Madgraph.
base_dir = f"{main}/mg5/C_{Wils}/pp_cee" 
folders = glob.glob(os.path.join(base_dir, "C_*")) 

#Vrednosti Wilsonovih koeficientov, pri katerih smo generirali dogodke
c_data = []
for folder in folders:
    name = os.path.basename(folder)
    match = re.match(r"C_([\d.]+)", name)
    if match:
        c_data.append((float(match.group(1)), match.group(1)))
c_data.sort(key=lambda x: x[0])
c_values = [c[0] for c in c_data]   #Številčne vrednosti - za graf
c_strings = [c[1] for c in c_data]  #Besedilne vrednosti - za poti do result.dat datotek

#Izračunana asimetrija za vsako vrednost koeficienta
asymetry_values = []
for c_val, c_str in zip(c_values, c_strings):
    file_sm = f"{main}/mg5/SM/wils_electron/SubProcesses/results.dat"
    file_c  = f"{main}/mg5/C_{Wils}/pp_cee/C_{c_str}/SubProcesses/results.dat"
    file_anti_c = f"{main}/mg5/C_{Wils}/pp_c~ee/C_{c_str}/SubProcesses/results.dat"
    asymetry_values.append(asymetry(file_sm, file_c, file_anti_c, c_val))
asymetry_values = np.array(asymetry_values)

#Oznaka na grafu
label = rf"$C_{{{Wils[:-1]}}}^{{(1)}}$"

plt.plot(c_values, asymetry_values, color="black", label=label)

#Meja na Wilsonov koeficient
label = rf"meja $C_{{{Wils[:-1]}}}^{{(1)}}$"
plt.vlines(meje[Wils], -0.05, 1, color=colors1[2], label=label)

#Logaritemska skala                   
plt.xscale("log", base=10)
plt.yscale("log", base=10)

plt.xlabel("$C$ [TeV$^{-2}$]")
plt.ylabel(r"$\frac{\sigma_c - \sigma_{\bar{c}}}{\sigma_c + \sigma_{\bar{c}}}$")
plt.ylim((1e-12,1))
plt.legend(loc="lower right")
plt.savefig(fig_path)
plt.show()
