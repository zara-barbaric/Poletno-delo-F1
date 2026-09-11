import numpy as np
import matplotlib.pyplot as plt
import os
import re
import glob


###ZA SPREMENITI:
#Pot do mape s celotnim projektom
main = "/scratch/barbariczara/2026"
#Vrednost Wilsonovega koeficienta
C=0.1
#Pot do končne slike 
fig_path = f"{main}/graphs/pt_photon_C_{C}.png"

#Izgled grafa
colors1 = plt.cm.Set2(np.linspace(0, 1, 8))[2:]
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




#Za vsak Wilsonov koeficient izračuna asimetrijo in nariše graf
plt.gca().set_prop_cycle(color=colors1)
for Wils in ["uW", "uB"]:

    #Poišče mape oblike pt_*, kjer je * vrednost gibalen količine. To so mape, ki jih določimo kot output v Madgraph.
    base_dir = f"{main}/mg5/C_{Wils}/pp_ca/meja/C_{C}"
    folders = glob.glob(os.path.join(base_dir, "pt_*"))
    
    #Vrednosti gibalne količine, pri katerih smo generirali dogodke.
    pt_data = []
    for folder in folders:
        name = os.path.basename(folder)
        match = re.match(r"pt_([\d.]+)", name)
        if match:
            pt_data.append((float(match.group(1)), match.group(1)))
    pt_data.sort(key=lambda x: x[0]) 
    pt_values = [pt[0] for pt in pt_data]   #Številčne vrednosti - za graf
    pt_strings = [pt[1] for pt in pt_data]  #Besedilne vrednosti - za poti do result.dat datotek

    #Izračunana asimetrija za vsako vrednost koeficienta
    asymetry_values = []
    for pt_val, pt_str in zip(pt_values, pt_strings):
        file_sm = f"{main}/mg5/SM/pt_photon/pt_{pt_str}/SubProcesses/results.dat"
        file_c  = f"{main}/mg5/C_{Wils}/pp_ca/meja/C_{C}/pt_{pt_str}/SubProcesses/results.dat"
        file_c_ = f"{main}/mg5/C_{Wils}/pp_c~a/meja/C_{C}/pt_{pt_str}/SubProcesses/results.dat"
        asymetry_values.append(asymetry(file_sm, file_c, file_c_, pt_val))
    asymetry_values = np.array(asymetry_values)

    label = rf"$C_{{{Wils}}}$"

    plt.plot(pt_values[6:57], asymetry_values[6:57], label=label)

plt.yscale("log", base=10)

plt.xlabel("$p_T$ [GeV]")                                                               
plt.ylabel(r"$\frac{\sigma_c - \sigma_{\bar{c}}}{\sigma_c + \sigma_{\bar{c}}}$")
plt.xticks((50,100,150,200,250,300),("50","100","150","200","250","300"))
plt.title(rf"$C_{{{C}}}$")
plt.legend()
plt.savefig(fig_path)
plt.show()
