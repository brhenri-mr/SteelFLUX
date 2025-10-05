import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot(dados, materiais):

    df = pd.DataFrame(dados)

    # ===== VISUALIZAÇÃO 1: Scatter Plot Multi-dimensional =====
    fig, ax = plt.subplots(figsize=(16, 9))

    # Cores baseadas no material
    material_colors = {'ASTM A36': '#FF6B6B', 'ASTM A572 Gr50': '#4ECDC4', 'ASTM A992': '#45B7D1'}
    colors = df['material'].map(material_colors)

    # Tamanho baseado no diâmetro do parafuso
    sizes = (df['diametro_parafuso'] / 12.7) ** 2 * 100

    # Plot principal: Espessura vs Número de Parafusos
    # Opacidade baseada no FS (maior FS = mais opaco)
    alphas = (df['FS'] - df['FS'].min()) / (df['FS'].max() - df['FS'].min()) * 0.7 + 0.3

    for idx, row in df.iterrows():
        ax.scatter(row['num_parafusos'], row['espessura_chapa'],
                c=colors[idx], s=sizes[idx], alpha=alphas[idx],
                edgecolors='black', linewidth=0.5)

    # Configurações
    ax.set_xlabel('Número de Parafusos', fontsize=13, fontweight='bold')
    ax.set_ylabel('Espessura da Chapa (mm)', fontsize=13, fontweight='bold')
    ax.set_title('Correlação: Material × Espessura × Parafusos × Diâmetro × FS\n(Cor = Material | Tamanho = Diâmetro | Opacidade = FS)', 
                fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Legenda de materiais
    from matplotlib.patches import Patch
    legend_materials = [Patch(facecolor=material_colors[mat], edgecolor='black', label=mat) 
                    for mat in materiais]
    legend1 = ax.legend(handles=legend_materials, title='Material da Chapa', 
                    loc='upper left', fontsize=10, title_fontsize=11)

    # Legenda de diâmetros
    from matplotlib.lines import Line2D
    diametros_unicos = sorted(df['diametro_parafuso'].unique())
    legend_diam = [Line2D([0], [0], marker='o', color='w', 
                        markerfacecolor='gray', 
                        markersize=np.sqrt((d/12.7)**2 * 100)/2,
                        markeredgecolor='black',
                        label=f'Ø {d:.1f} mm') 
                for d in diametros_unicos]
    legend2 = ax.legend(handles=legend_diam, title='Diâmetro Parafuso', 
                    loc='lower right', fontsize=10, title_fontsize=11)

    ax.add_artist(legend1)

    # Anotação sobre opacidade
    ax.text(0.02, 0.98, 'Opacidade: quanto mais opaco, maior o FS', 
            transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.show()


