import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns
from typing import Dict, List, Tuple

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class StratificationAnalyzer:
    """
    Classe para análise e visualização de estratificação de conexões metálicas
    """
    
    def __init__(self, data: Dict[str, List]):
        """
        Inicializa o analisador com os dados
        
        Args:
            data: Dicionário com listas de material, espessura_chapa, 
                  num_parafusos, diametro_parafuso, FS
        """
        self.df = pd.DataFrame(data)
        self._create_stratification()
        
    def _create_stratification(self):
        """Cria categorias de estratificação"""
        # Categorizar FS
        self.df['FS_categoria'] = pd.cut(
            self.df['FS'], 
            bins=[0, 0.3, 0.6, 0.8, 1.0],
            labels=['(0.0-0.3)', '(0.3-0.6)', 
                    '(0.6-0.8)', '(0.8-1.0)'],
            include_lowest=True
        )
        
        # Categorizar número de parafusos
        self.df['grupo_parafusos'] = pd.cut(
            self.df['num_parafusos'],
            bins=[0, 2, 4, 6, 8],
            labels=['2 parafusos', '4 parafusos', 
                    '6 parafusos', '8 parafusos'],
            include_lowest=True
        )
        
    def generate_stratification_matrix(self, save_path: str = None):
        """
        Gera matriz de estratificação visual
        
        Args:
            save_path: Caminho para salvar a figura (opcional)
        """
        materiais = self.df['material'].unique()
        n_materiais = len(materiais)
        
        fig, axes = plt.subplots(n_materiais, 1, figsize=(14, 5*n_materiais))
        if n_materiais == 1:
            axes = [axes]
        
        for idx, material in enumerate(materiais):
            df_material = self.df[self.df['material'] == material]
            
            # Criar pivot table
            pivot = df_material.groupby(['grupo_parafusos', 'FS_categoria']).size().unstack(fill_value=0)
            
            # Reordenar colunas
            ordem_fs = ['(0.0-0.3)', '(0.3-0.6)', 
                        '(0.6-0.8)', '(0.8-1.0)']
            pivot = pivot.reindex(columns=ordem_fs, fill_value=0)
            
            # Criar heatmap
            sns.heatmap(
                pivot, 
                annot=True, 
                fmt='d', 
                cmap='Blues',
                cbar_kws={'label': 'Número de Amostras'},
                ax=axes[idx],
                linewidths=1,
                linecolor='white'
            )
            
            axes[idx].set_title(f'Material: {material} (Total: {len(df_material)} amostras)', 
                               fontsize=14, fontweight='bold', pad=10)
            axes[idx].set_xlabel('Fator de Segurança', fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('Configuração de Parafusos', fontsize=12, fontweight='bold')
            
            # Adicionar totais
            totais_col = pivot.sum(axis=0)
            totais_row = pivot.sum(axis=1)
            
            # Texto com totais no eixo
            for i, total in enumerate(totais_row):
                axes[idx].text(len(pivot.columns) + 0.5, i + 0.5, f'{int(total)}',
                              ha='center', va='center', fontweight='bold', fontsize=10)
            
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Matriz salva em: {save_path}")
        
        plt.show()
        
    def generate_distribution_histograms(self, save_path: str = None):
        """
        Gera histogramas de distribuição
        
        Args:
            save_path: Caminho para salvar a figura (opcional)
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Distribuição do Banco de Dados de Conexões Metálicas', 
                     fontsize=16, fontweight='bold', y=1.00)
        
        # 1. Distribuição de FS
        axes[0, 0].hist(self.df['FS'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(self.df['FS'].mean(), color='red', linestyle='--', 
                          label=f'Média: {self.df["FS"].mean():.3f}')
        axes[0, 0].set_xlabel('Fator de Segurança (FS)', fontweight='bold')
        axes[0, 0].set_ylabel('Frequência', fontweight='bold')
        axes[0, 0].set_title('Distribuição de FS')
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # 2. Distribuição por categoria de FS
        fs_counts = self.df['FS_categoria'].value_counts().sort_index()
        axes[0, 1].bar(range(len(fs_counts)), fs_counts.values, 
                      color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'],
                      edgecolor='black', alpha=0.7)
        axes[0, 1].set_xticks(range(len(fs_counts)))
        axes[0, 1].set_xticklabels(fs_counts.index, rotation=45, ha='right')
        axes[0, 1].set_ylabel('Número de Amostras', fontweight='bold')
        axes[0, 1].set_title('Distribuição por Categoria de FS')
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for i, v in enumerate(fs_counts.values):
            axes[0, 1].text(i, v + max(fs_counts.values)*0.02, str(v), 
                           ha='center', va='bottom', fontweight='bold')
        
        # 3. Distribuição de número de parafusos
        parafusos_counts = self.df['num_parafusos'].value_counts().sort_index()
        axes[0, 2].bar(parafusos_counts.index, parafusos_counts.values, 
                      color='teal', edgecolor='black', alpha=0.7)
        axes[0, 2].set_xlabel('Número de Parafusos', fontweight='bold')
        axes[0, 2].set_ylabel('Frequência', fontweight='bold')
        axes[0, 2].set_title('Distribuição de Parafusos')
        axes[0, 2].grid(axis='y', alpha=0.3)
        
        # 4. Distribuição por material
        material_counts = self.df['material'].value_counts()
        axes[1, 0].barh(range(len(material_counts)), material_counts.values, 
                       color='coral', edgecolor='black', alpha=0.7)
        axes[1, 0].set_yticks(range(len(material_counts)))
        axes[1, 0].set_yticklabels(material_counts.index)
        axes[1, 0].set_xlabel('Número de Amostras', fontweight='bold')
        axes[1, 0].set_title('Distribuição por Material')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # Adicionar valores nas barras
        for i, v in enumerate(material_counts.values):
            axes[1, 0].text(v + max(material_counts.values)*0.02, i, str(v), 
                           va='center', fontweight='bold')
        
        # 5. Distribuição de espessura de chapa
        axes[1, 1].hist(self.df['espessura_chapa'], bins=15, 
                       color='mediumpurple', edgecolor='black', alpha=0.7)
        axes[1, 1].axvline(self.df['espessura_chapa'].mean(), color='red', 
                          linestyle='--', 
                          label=f'Média: {self.df["espessura_chapa"].mean():.2f}mm')
        axes[1, 1].set_xlabel('Espessura da Chapa (mm)', fontweight='bold')
        axes[1, 1].set_ylabel('Frequência', fontweight='bold')
        axes[1, 1].set_title('Distribuição de Espessura')
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
        
        # 6. Distribuição de diâmetro de parafuso
        diametro_counts = self.df['diametro_parafuso'].value_counts().sort_index()
        axes[1, 2].bar(diametro_counts.index, diametro_counts.values, 
                      color='goldenrod', edgecolor='black', alpha=0.7)
        axes[1, 2].set_xlabel('Diâmetro do Parafuso (mm)', fontweight='bold')
        axes[1, 2].set_ylabel('Frequência', fontweight='bold')
        axes[1, 2].set_title('Distribuição de Diâmetros')
        axes[1, 2].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Histogramas salvos em: {save_path}")
        
        plt.show()
        
    def generate_stacked_bar_chart(self, save_path: str = None):
        """
        Gera gráfico de barras empilhadas por material
        
        Args:
            save_path: Caminho para salvar a figura (opcional)
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Criar pivot para barras empilhadas
        pivot = self.df.groupby(['FS_categoria', 'material']).size().unstack(fill_value=0)
        
        # Reordenar índice
        ordem_fs = ['(0.0-0.3)', '(0.3-0.6)', 
                    '(0.6-0.8)', '(0.8-1.0)']
        pivot = pivot.reindex(ordem_fs, fill_value=0)
        
        # Plotar
        pivot.plot(kind='bar', stacked=True, ax=ax, 
                  color=['#3b82f6', '#10b981', '#f59e0b'], 
                  edgecolor='black', linewidth=1.5, alpha=0.8)
        
        ax.set_xlabel('Faixa de Fator de Segurança', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Amostras', fontsize=12, fontweight='bold')
        ax.set_title('Distribuição de Amostras por FS e Material', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.legend(title='Material', title_fontsize=11, fontsize=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for container in ax.containers:
            ax.bar_label(container, label_type='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de barras salvo em: {save_path}")
        
        plt.show()
        
    def generate_summary_table(self) -> pd.DataFrame:
        """
        Gera tabela resumo da estratificação
        
        Returns:
            DataFrame com estatísticas de estratificação
        """
        summary = self.df.groupby(['material', 'grupo_parafusos', 'FS_categoria']).agg({
            'FS': ['count', 'mean', 'std', 'min', 'max'],
            'espessura_chapa': 'mean',
            'diametro_parafuso': 'mean'
        }).round(3)
        
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        summary = summary.reset_index()
        
        # Renomear colunas
        summary.columns = [
            'Material', 'Grupo_Parafusos', 'FS_Categoria', 
            'N_Amostras', 'FS_Média', 'FS_DesvioPadrão', 'FS_Min', 'FS_Max',
            'Espessura_Média', 'Diametro_Médio'
        ]
        
        return summary
    
    def print_stratification_report(self):
        """Imprime relatório completo de estratificação"""
        print("="*80)
        print("RELATÓRIO DE ESTRATIFICAÇÃO - CONEXÕES METÁLICAS".center(80))
        print("="*80)
        print()
        
        print(f"📊 Total de amostras: {len(self.df)}")
        print()
        
        print("📋 Distribuição por Material:")
        print(self.df['material'].value_counts().to_string())
        print()
        
        print("🔩 Distribuição por Número de Parafusos:")
        print(self.df['num_parafusos'].value_counts().sort_index().to_string())
        print()
        
        print("⚡ Distribuição por Categoria de FS:")
        print(self.df['FS_categoria'].value_counts().sort_index().to_string())
        print()
        
        print("📈 Estatísticas de FS:")
        print(self.df['FS'].describe().to_string())
        print()
        
        # Número de estratos
        n_estratos = self.df.groupby(['material', 'grupo_parafusos', 'FS_categoria']).size()
        n_estratos_total = len(n_estratos)
        n_estratos_vazios = sum(n_estratos == 0)
        
        print(f"🎯 Número de estratos:")
        print(f"   - Total possível: {n_estratos_total}")
        print(f"   - Com amostras: {n_estratos_total - n_estratos_vazios}")
        print(f"   - Vazios: {n_estratos_vazios}")
        print()
        
        print("⚠️  Estratos com poucas amostras (< 10):")
        estratos_poucos = n_estratos[n_estratos < 10]
        if len(estratos_poucos) > 0:
            for idx, count in estratos_poucos.items():
                print(f"   - {idx}: {count} amostras")
        else:
            print("   ✓ Nenhum estrato com menos de 10 amostras")
        print()
        
        print("="*80)


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