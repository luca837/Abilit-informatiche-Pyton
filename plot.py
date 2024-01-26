
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import numpy as np
import sys


def read_file(path):
    with open(path, 'r') as f:
        header = f.readline()
        header = header[1:].strip().split()
    
    raw_data = np.loadtxt(path, comments='#')
    data = dict()
    for i, name in enumerate(header):
        data[name] = raw_data[:, i]
            
    return data


def plot_color_mag(M_ass, b_y, age_parent):
    # calcola i bins
    bin_edges = np.histogram_bin_edges(
        age_parent,
        bins='auto',
        range=(age_parent.min(), age_parent.max()+1e-2)
    )

    # calcola il bin a cui appartiene ogni stella
    mapping = np.digitize(age_parent, bin_edges)
    
    plt.figure(figsize=(10,8))
    sc = plt.scatter(b_y, -M_ass, s=2, c=mapping)
    plt.legend(
        handles=[Patch(color=sc.to_rgba(v), label=f'{bin_edges[v-1]:.2f} Gyr - {bin_edges[v]:.2f} Gyr')
                for v in set(mapping)],
        bbox_to_anchor=(1.25, 1.01),
        frameon=False,
        fontsize=8,
    )
    plt.title('Diagramma colore-magnitudine', fontsize=15)
    plt.tight_layout()
    plt.savefig('plot_color_mag.png')


def plot_metal_dist(MsuH, age_parent):
    samples = [age_parent < 1, (1 <= age_parent) & (age_parent <= 5), age_parent > 5]
    titles = ['< 1 Gyr', '1 - 5 Gyr', '> 5 Gyr']
    colors = ['red', 'orange', 'gold']

    plt.subplots(1,3, figsize=(11, 5))

    for i in range(len(samples)):
        plt.subplot(1,3,i+1)
        plt.hist(MsuH[samples[i]], bins=12, label=titles[i], color=colors[i], edgecolor='k', linewidth=0.5)
        plt.axvline(MsuH[samples[0]].mean(), label='mean', color='lime', zorder=10, linewidth=2, linestyle='--')
        plt.axvline(np.median(MsuH[samples[0]]), label='median', color='blue', zorder=10, linewidth=2, linestyle='-.')
        plt.xlabel('$M_{suH}$')
        plt.legend(frameon=False)

    plt.suptitle('Distribuzione metallicità', fontsize=15)
    plt.tight_layout()
    plt.savefig('plot_metal_dist.png')


def plot_metal_mass(MsuH, m_ini, age_parent):
    samples = [age_parent < 1, (1 <= age_parent) & (age_parent <= 5), age_parent > 5]
    titles = ['< 1 Gyr', '1 - 5 Gyr', '> 5 Gyr']
    colors = ['purple', 'red', 'orange']
    
    plt.subplots(2,3, figsize=(11, 8))

    for i in range(len(samples)):
        plt.subplot(2,3,i+1)
        plt.scatter(m_ini[samples[i]], MsuH[samples[i]], label=titles[i], color=colors[i], s=5)
        if i == 0:
            plt.ylabel('$M_{suH}$')
        plt.xlabel('$M_{ini}$')
        plt.legend(handles=[Patch(color=colors[i], label=titles[i])], frameon=False, loc='lower right')

    for i in range(len(samples)):
        plt.subplot(2,3,i+4)
        H, yedges, xedges = np.histogram2d(MsuH[samples[i]], m_ini[samples[i]], bins=20)
        plt.pcolormesh(xedges, yedges, H, cmap='viridis')
        plt.xlim(m_ini[samples[i]].min(), m_ini[samples[i]].max())
        plt.ylim(MsuH[samples[i]].min(), MsuH[samples[i]].max())
        if i == 0:
            plt.ylabel('$M_{suH}$')
        plt.xlabel('$M_{ini}$')
        plt.legend(handles=[Patch(color=colors[i], label=titles[i])], loc='lower right', framealpha=1)

    plt.suptitle('Metallicità in funzione della massa iniziale', fontsize=15)
    plt.tight_layout()
    plt.savefig('plot_metal_mass.png')
    

if __name__ == '__main__':
    # controlla che il file sia stato passato come argomento
    if len(sys.argv) != 2:
        print('Uso dello script: python plot.py <file>')
        sys.exit(1)
    
    # leggi il file e restituisci un dizionario con i dati
    data = read_file(sys.argv[1])

    # diagramma colore-magnitudine
    plot_color_mag(data['M_ass'], data['b-y'], data['age_parent'])

    # distribuzione metallicità in funzione dell'età
    plot_metal_dist(data['MsuH'], data['age_parent'])
    
    # metallicità in funzione della massa iniziale
    plot_metal_mass(data['MsuH'], data['m_ini'], data['age_parent'])


