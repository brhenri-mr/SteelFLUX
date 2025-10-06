import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot(dados, materiais):


	df = pd.DataFrame(dados)

	# ===== VISUALIZAÇÃO: Scatter Plot Multi-dimensional =====
	fig, ax = plt.subplots(figsize=(16, 9))

	# Cores baseadas no material
	material_colors = {'A36': '#FF6B6B', 'A572_GR50': '#FFDE21', 'A572_GR55': '#45B7D1'}
	colors = df['material'].map(material_colors)

	# Tamanho baseado no diâmetro do parafuso
	sizes = (df['diametro_parafuso'] / 12.7) ** 2 * 100

	# Opacidade baseada na espessura da chapa (chapas mais espessas = mais opaco)
	alphas = (df['espessura_chapa'] - df['espessura_chapa'].min()) / \
			(df['espessura_chapa'].max() - df['espessura_chapa'].min()) * 0.6 + 0.3

	# Plot principal: Número de Parafusos vs FS
	for idx, row in df.iterrows():
		ax.scatter(row['num_parafusos'], row['FS'],
				c=colors[idx], s=sizes[idx], alpha=alphas[idx],
				edgecolors='black', linewidth=0.5)

	# Configurações
	ax.set_xlabel('Número de Parafusos', fontsize=13, fontweight='bold')
	ax.set_ylabel('Fator de Segurança (FS)', fontsize=13, fontweight='bold')
	ax.set_title('Distribuição de Conexões', 
				fontsize=15, fontweight='bold', pad=20)
 
	
	# DEFININDO OS TICKS DO EIXO X - SÓ 2, 4, 6, 8
	ax.set_xticks([2, 4, 6, 8, 10])
	ax.set_xlim(1, 9)  # Dar um pouco de espaço nas bordas


	# Legenda de materiais
	from matplotlib.patches import Patch
	legend_materials = [Patch(facecolor=material_colors[mat], edgecolor='black', label=mat) 
					for mat in materiais]
	legend1 = ax.legend(handles=legend_materials, title='Material da Chapa', 
					loc='upper right', fontsize=10, title_fontsize=11)

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
	ax.text(0.02, 0.98, 'Opacidade: quanto mais opaco, menor a espessura da chapa', 
			transform=ax.transAxes, fontsize=10, 
			verticalalignment='top', style='italic',
			bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

	plt.tight_layout()
	plt.show()