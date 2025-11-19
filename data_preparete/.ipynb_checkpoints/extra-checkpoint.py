import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
from mpl_toolkits.mplot3d import Axes3D

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class StratificationAnalyzerExtra:
    """
    Classe para análise e visualização de estratificação de conexões metálicas
    com foco em espessura variável
    """
    
    def __init__(self, data: Dict[str, List], fixed_material: str = 'ASTM A36', 
                 fixed_diameter: float = 16.0):
        """
        Inicializa o analisador com os dados
        
        Args:
            data: Dicionário com listas de material, espessura_chapa, 
                  num_parafusos, diametro_parafuso, FS
            fixed_material: Material fixo para análise
            fixed_diameter: Diâmetro fixo do parafuso (mm)
        """
        self.df = pd.DataFrame(data)
        self.fixed_material = fixed_material
        self.fixed_diameter = fixed_diameter
        
        # Criar dataframe completo
        self.df_full = self.df.copy()
        
        # Filtrar para subconjunto fixado
        self.df_subset = self.df[
            (self.df['material'] == fixed_material) & 
            (self.df['diametro_parafuso'] == fixed_diameter)
        ].copy()
        
        self._create_stratification()
        
    def _create_stratification(self):
        """Cria categorias de estratificação"""
        for df in [self.df_full, self.df_subset]:
            # Categorizar FS
            df['FS_categoria'] = pd.cut(
                df['FS'], 
                bins=[0, 0.3, 0.6, 0.8, 1.0],
                labels=['Crítico (0.0-0.3)', 'Baixo (0.3-0.6)', 
                        'Adequado (0.6-0.8)', 'Confortável (0.8-1.0)'],
                include_lowest=True
            )
            
            # Categorizar número de parafusos
            df['grupo_parafusos'] = pd.cut(
                df['num_parafusos'],
                bins=[0, 2, 4, 6, 8],
                labels=['2 parafusos', '3-4 parafusos', 
                        '5-6 parafusos', '7-8 parafusos'],
                include_lowest=True
            )
            
            # Categorizar espessura
            df['espessura_label'] = df['espessura_chapa'].apply(
                lambda x: f'{x:.2f}mm'
            )
    
    def generate_comparative_overview(self, save_path: str = None):
        """
        Gera visão comparativa: banco completo vs. subconjunto filtrado
        """
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle('Comparação: Banco Completo vs. Subconjunto de Treinamento', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Layout: 2 linhas x 3 colunas
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # ========== LINHA 1: BANCO COMPLETO ==========
        
        # 1.1 Distribuição de FS - Completo
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(self.df_full['FS'], bins=30, color='steelblue', 
                edgecolor='black', alpha=0.7, label='Banco Completo')
        ax1.axvline(self.df_full['FS'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Média: {self.df_full["FS"].mean():.3f}')
        ax1.set_xlabel('Fator de Segurança (FS)', fontweight='bold')
        ax1.set_ylabel('Frequência', fontweight='bold')
        ax1.set_title(f'Banco Completo (n={len(self.df_full)})', fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # 1.2 Distribuição por Material - Completo
        ax2 = fig.add_subplot(gs[0, 1])
        material_counts = self.df_full['material'].value_counts()
        colors_mat = ['#3b82f6', '#10b981', '#f59e0b']
        bars = ax2.bar(range(len(material_counts)), material_counts.values, 
                      color=colors_mat[:len(material_counts)], 
                      edgecolor='black', alpha=0.7)
        ax2.set_xticks(range(len(material_counts)))
        ax2.set_xticklabels(material_counts.index, rotation=0)
        ax2.set_ylabel('Número de Amostras', fontweight='bold')
        ax2.set_title('Distribuição por Material', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Destacar material fixado
        for i, mat in enumerate(material_counts.index):
            if mat == self.fixed_material:
                bars[i].set_edgecolor('red')
                bars[i].set_linewidth(3)
        
        for i, v in enumerate(material_counts.values):
            ax2.text(i, v + max(material_counts.values)*0.02, str(v), 
                    ha='center', va='bottom', fontweight='bold')
        
        # 1.3 Distribuição de Espessuras - Completo
        ax3 = fig.add_subplot(gs[0, 2])
        espessura_counts = self.df_full['espessura_chapa'].value_counts().sort_index()
        ax3.bar(espessura_counts.index, espessura_counts.values, 
               color='teal', edgecolor='black', alpha=0.7, width=1.5)
        ax3.set_xlabel('Espessura da Chapa (mm)', fontweight='bold')
        ax3.set_ylabel('Frequência', fontweight='bold')
        ax3.set_title('Distribuição de Espessuras', fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # ========== LINHA 2: SUBCONJUNTO FILTRADO ==========
        
        # 2.1 Distribuição de FS - Subconjunto
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.hist(self.df_subset['FS'], bins=20, color='coral', 
                edgecolor='black', alpha=0.7, label='Subconjunto')
        ax4.axvline(self.df_subset['FS'].mean(), color='darkred', linestyle='--', 
                   linewidth=2, label=f'Média: {self.df_subset["FS"].mean():.3f}')
        
        # Overlay da distribuição completa (transparente)
        ax4.hist(self.df_full['FS'], bins=30, color='steelblue', 
                edgecolor='none', alpha=0.2, label='Banco Completo (ref.)')
        
        ax4.set_xlabel('Fator de Segurança (FS)', fontweight='bold')
        ax4.set_ylabel('Frequência', fontweight='bold')
        ax4.set_title(f'Subconjunto Filtrado (n={len(self.df_subset)})', 
                     fontweight='bold', color='darkred')
        ax4.legend()
        ax4.grid(alpha=0.3)
        
        # 2.2 Info Box - Parâmetros Fixados
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.axis('off')
        
        info_text = f"""
        PARÂMETROS FIXADOS
        {'='*35}
        
        Material: {self.fixed_material}
        Bitola: φ{self.fixed_diameter}mm
        
        {'='*35}
        PARÂMETROS VARIÁVEIS
        {'='*35}
        
        Espessura: {self.df_subset['espessura_chapa'].min():.2f} - {self.df_subset['espessura_chapa'].max():.2f}mm
        Parafusos: {int(self.df_subset['num_parafusos'].min())} - {int(self.df_subset['num_parafusos'].max())} unidades
        FS: {self.df_subset['FS'].min():.3f} - {self.df_subset['FS'].max():.3f}
        
        {'='*35}
        AMOSTRAS DISPONÍVEIS
        {'='*35}
        
        Banco completo: {len(self.df_full)}
        Subconjunto: {len(self.df_subset)}
        Redução: {(1 - len(self.df_subset)/len(self.df_full))*100:.1f}%
        """
        
        ax5.text(0.1, 0.5, info_text, transform=ax5.transAxes,
                fontsize=11, verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 2.3 Distribuição de Espessuras - Subconjunto
        ax6 = fig.add_subplot(gs[1, 2])
        espessura_subset = self.df_subset['espessura_chapa'].value_counts().sort_index()
        ax6.bar(espessura_subset.index, espessura_subset.values, 
               color='coral', edgecolor='black', alpha=0.7, width=1.5)
        ax6.set_xlabel('Espessura da Chapa (mm)', fontweight='bold')
        ax6.set_ylabel('Frequência', fontweight='bold')
        ax6.set_title('Espessuras no Subconjunto (VARIÁVEL)', 
                     fontweight='bold', color='darkred')
        ax6.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Comparação salva em: {save_path}")
        
        plt.show()
    
    def generate_3d_stratification_matrix(self, save_path: str = None):
        """
        Gera matriz de estratificação 3D: espessura × num_parafusos × FS
        """
        # Preparar dados
        pivot_data = []
        espessuras = sorted(self.df_subset['espessura_chapa'].unique())
        num_parafusos_vals = sorted(self.df_subset['num_parafusos'].unique())
        
        fig, axes = plt.subplots(len(espessuras), 1, 
                                figsize=(14, 5*len(espessuras)))
        if len(espessuras) == 1:
            axes = [axes]
        
        fig.suptitle(f'Matriz de Estratificação - {self.fixed_material}, φ{self.fixed_diameter}mm\n' +
                    'Espessura VARIÁVEL', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        for idx, esp in enumerate(espessuras):
            df_esp = self.df_subset[self.df_subset['espessura_chapa'] == esp]
            
            # Criar pivot table
            pivot = df_esp.groupby(['num_parafusos', 'FS_categoria']).size().unstack(fill_value=0)
            
            # Reordenar colunas
            ordem_fs = ['Crítico (0.0-0.3)', 'Baixo (0.3-0.6)', 
                        'Adequado (0.6-0.8)', 'Confortável (0.8-1.0)']
            pivot = pivot.reindex(columns=ordem_fs, fill_value=0)
            pivot = pivot.reindex(index=num_parafusos_vals, fill_value=0)
            
            # Criar heatmap
            sns.heatmap(
                pivot, 
                annot=True, 
                fmt='d', 
                cmap='YlOrRd',
                cbar_kws={'label': 'Número de Amostras'},
                ax=axes[idx],
                linewidths=1.5,
                linecolor='white',
                vmin=0,
                vmax=max(30, pivot.max().max())
            )
            
            axes[idx].set_title(f'Espessura: {esp:.2f}mm (Total: {len(df_esp)} amostras)', 
                               fontsize=13, fontweight='bold', pad=10)
            axes[idx].set_xlabel('Categoria de Fator de Segurança', 
                                fontsize=11, fontweight='bold')
            axes[idx].set_ylabel('Número de Parafusos', 
                                fontsize=11, fontweight='bold')
            axes[idx].set_yticklabels(axes[idx].get_yticklabels(), rotation=0)
            
            # Adicionar totais por linha
            totais_row = pivot.sum(axis=1)
            for i, (paraf, total) in enumerate(totais_row.items()):
                axes[idx].text(len(pivot.columns) + 0.3, i + 0.5, f'Σ={int(total)}',
                              ha='left', va='center', fontweight='bold', 
                              fontsize=10, color='darkred')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Matriz 3D salva em: {save_path}")
        
        plt.show()
    
    def generate_correlation_analysis(self, save_path: str = None):
        """
        Análise de correlação entre variáveis no subconjunto
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle(f'Análise de Correlações - Subconjunto de Treinamento', 
                     fontsize=16, fontweight='bold')
        
        # 1. FS vs Espessura (scatter)
        ax1 = axes[0, 0]
        scatter = ax1.scatter(self.df_subset['espessura_chapa'], 
                             self.df_subset['FS'],
                             c=self.df_subset['num_parafusos'], 
                             cmap='viridis', 
                             s=100, alpha=0.6, edgecolors='black')
        ax1.set_xlabel('Espessura da Chapa (mm)', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Fator de Segurança (FS)', fontweight='bold', fontsize=11)
        ax1.set_title('Correlação: Espessura × FS', fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # Calcular correlação
        corr = self.df_subset['espessura_chapa'].corr(self.df_subset['FS'])
        ax1.text(0.05, 0.95, f'ρ = {corr:.3f}', transform=ax1.transAxes,
                fontsize=12, verticalalignment='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Num. Parafusos', fontweight='bold')
        
        # 2. FS vs Num Parafusos (boxplot)
        ax2 = axes[0, 1]
        self.df_subset.boxplot(column='FS', by='num_parafusos', ax=ax2)
        ax2.set_xlabel('Número de Parafusos', fontweight='bold', fontsize=11)
        ax2.set_ylabel('Fator de Segurança (FS)', fontweight='bold', fontsize=11)
        ax2.set_title('Distribuição de FS por Quantidade de Parafusos', fontweight='bold')
        ax2.get_figure().suptitle('')  # Remove título automático do boxplot
        ax2.grid(alpha=0.3)
        
        # 3. Heatmap de contagem: Espessura × Num Parafusos
        ax3 = axes[1, 0]
        pivot_count = self.df_subset.groupby(['espessura_chapa', 'num_parafusos']).size().unstack(fill_value=0)
        sns.heatmap(pivot_count, annot=True, fmt='d', cmap='Blues', 
                   ax=ax3, cbar_kws={'label': 'Num. Amostras'})
        ax3.set_xlabel('Número de Parafusos', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Espessura (mm)', fontweight='bold', fontsize=11)
        ax3.set_title('Distribuição: Espessura × Parafusos', fontweight='bold')
        
        # 4. Histograma 2D: Espessura × FS
        ax4 = axes[1, 1]
        h = ax4.hist2d(self.df_subset['espessura_chapa'], 
                      self.df_subset['FS'],
                      bins=[len(self.df_subset['espessura_chapa'].unique()), 20],
                      cmap='YlOrRd', edgecolors='black')
        ax4.set_xlabel('Espessura da Chapa (mm)', fontweight='bold', fontsize=11)
        ax4.set_ylabel('Fator de Segurança (FS)', fontweight='bold', fontsize=11)
        ax4.set_title('Densidade: Espessura × FS', fontweight='bold')
        cbar2 = plt.colorbar(h[3], ax=ax4)
        cbar2.set_label('Frequência', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Análise de correlação salva em: {save_path}")
        
        plt.show()
    
    def select_training_samples(self, n_samples: int = 60, 
                               n_percentiles: int = 5) -> pd.DataFrame:
        """
        Seleciona amostras estratificadas para treinamento
        
        Args:
            n_samples: Número total de amostras desejadas
            n_percentiles: Número de percentis de FS por estrato
            
        Returns:
            DataFrame com amostras selecionadas
        """
        espessuras = sorted(self.df_subset['espessura_chapa'].unique())
        num_parafusos_vals = sorted(self.df_subset['num_parafusos'].unique())
        
        # Calcular quantas configs por (espessura, num_parafusos)
        n_configs = len(espessuras) * len(num_parafusos_vals)
        samples_per_config = max(1, n_samples // n_configs)
        
        selected_samples = []
        
        for esp in espessuras:
            for n_paraf in num_parafusos_vals:
                # Filtrar estrato
                df_strata = self.df_subset[
                    (self.df_subset['espessura_chapa'] == esp) &
                    (self.df_subset['num_parafusos'] == n_paraf)
                ]
                
                if len(df_strata) == 0:
                    continue
                
                # Calcular percentis de FS
                if len(df_strata) >= n_percentiles:
                    percentiles = np.linspace(0, 100, n_percentiles)
                    fs_targets = np.percentile(df_strata['FS'], percentiles)
                    
                    # Selecionar amostra mais próxima de cada percentil
                    for fs_target in fs_targets:
                        idx = (df_strata['FS'] - fs_target).abs().idxmin()
                        selected_samples.append(df_strata.loc[idx])
                else:
                    # Se poucos dados, pegar todos
                    selected_samples.extend(df_strata.to_dict('records'))
        
        result_df = pd.DataFrame(selected_samples).drop_duplicates()
        
        # Ajustar para o número exato
        if len(result_df) > n_samples:
            result_df = result_df.sample(n=n_samples, random_state=42)
        
        return result_df.reset_index(drop=True)
    
    def visualize_selected_samples(self, selected_df: pd.DataFrame, 
                                   save_path: str = None):
        """
        Visualiza as amostras selecionadas para treinamento
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Amostras Selecionadas para Treinamento (n={len(selected_df)})', 
                     fontsize=16, fontweight='bold')
        
        # 1. Scatter: Espessura × FS (selecionadas vs. disponíveis)
        ax1 = axes[0, 0]
        ax1.scatter(self.df_subset['espessura_chapa'], self.df_subset['FS'],
                   c='lightgray', s=30, alpha=0.5, label='Disponíveis')
        ax1.scatter(selected_df['espessura_chapa'], selected_df['FS'],
                   c='red', s=150, marker='*', edgecolors='black', 
                   linewidths=1.5, label='Selecionadas', zorder=10)
        ax1.set_xlabel('Espessura (mm)', fontweight='bold')
        ax1.set_ylabel('FS', fontweight='bold')
        ax1.set_title('Distribuição Espacial das Amostras')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # 2. Distribuição por Espessura
        ax2 = axes[0, 1]
        esp_counts = selected_df['espessura_chapa'].value_counts().sort_index()
        ax2.bar(esp_counts.index, esp_counts.values, 
               color='coral', edgecolor='black', alpha=0.7, width=1.5)
        ax2.set_xlabel('Espessura (mm)', fontweight='bold')
        ax2.set_ylabel('Num. Amostras', fontweight='bold')
        ax2.set_title('Amostras por Espessura')
        ax2.grid(axis='y', alpha=0.3)
        
        for x, y in zip(esp_counts.index, esp_counts.values):
            ax2.text(x, y + 0.3, str(y), ha='center', fontweight='bold')
        
        # 3. Distribuição por Num Parafusos
        ax3 = axes[1, 0]
        paraf_counts = selected_df['num_parafusos'].value_counts().sort_index()
        ax3.bar(paraf_counts.index, paraf_counts.values, 
               color='teal', edgecolor='black', alpha=0.7)
        ax3.set_xlabel('Número de Parafusos', fontweight='bold')
        ax3.set_ylabel('Num. Amostras', fontweight='bold')
        ax3.set_title('Amostras por Configuração de Parafusos')
        ax3.grid(axis='y', alpha=0.3)
        
        for x, y in zip(paraf_counts.index, paraf_counts.values):
            ax3.text(x, y + 0.3, str(y), ha='center', fontweight='bold')
        
        # 4. Histograma de FS
        ax4 = axes[1, 1]
        ax4.hist(selected_df['FS'], bins=15, color='mediumpurple', 
                edgecolor='black', alpha=0.7)
        ax4.axvline(selected_df['FS'].mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Média: {selected_df["FS"].mean():.3f}')
        ax4.set_xlabel('Fator de Segurança (FS)', fontweight='bold')
        ax4.set_ylabel('Frequência', fontweight='bold')
        ax4.set_title('Distribuição de FS nas Amostras Selecionadas')
        ax4.legend()
        ax4.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Visualização de amostras selecionadas salva em: {save_path}")
        
        plt.show()
    
    def print_detailed_report(self, selected_df: pd.DataFrame = None):
        """Imprime relatório detalhado"""
        print("="*90)
        print("RELATÓRIO DE ESTRATIFICAÇÃO - CONEXÕES METÁLICAS (ESPESSURA VARIÁVEL)".center(90))
        print("="*90)
        print()
        
        print("📊 BANCO DE DADOS COMPLETO")
        print("-" * 90)
        print(f"Total de amostras: {len(self.df_full)}")
        print(f"Materiais: {', '.join(self.df_full['material'].unique())}")
        print(f"Range FS: {self.df_full['FS'].min():.3f} - {self.df_full['FS'].max():.3f}")
        print()
        
        print("🎯 SUBCONJUNTO FILTRADO")
        print("-" * 90)
        print(f"Material fixado: {self.fixed_material}")
        print(f"Diâmetro fixado: φ{self.fixed_diameter}mm")
        print(f"Total de amostras disponíveis: {len(self.df_subset)}")
        print(f"Redução: {(1 - len(self.df_subset)/len(self.df_full))*100:.1f}%")
        print()
        
        print("📏 ESPESSURAS DISPONÍVEIS (VARIÁVEL)")
        print("-" * 90)
        for esp in sorted(self.df_subset['espessura_chapa'].unique()):
            count = len(self.df_subset[self.df_subset['espessura_chapa'] == esp])
            print(f"  {esp:.2f}mm: {count} amostras")
        print()
        
        print("🔩 DISTRIBUIÇÃO POR NÚMERO DE PARAFUSOS")
        print("-" * 90)
        print(self.df_subset['num_parafusos'].value_counts().sort_index().to_string())
        print()
        
        print("⚡ ESTATÍSTICAS DE FS NO SUBCONJUNTO")
        print("-" * 90)
        print(self.df_subset['FS'].describe().to_string())
        print()
        
        # Análise de correlação
        corr_esp_fs = self.df_subset['espessura_chapa'].corr(self.df_subset['FS'])
        corr_paraf_fs = self.df_subset['num_parafusos'].corr(self.df_subset['FS'])
        
        print("📈 CORRELAÇÕES")
        print("-" * 90)
        print(f"Espessura × FS: ρ = {corr_esp_fs:.3f}")
        print(f"Num. Parafusos × FS: ρ = {corr_paraf_fs:.3f}")
        print()
        
        if selected_df is not None:
            print("✅ AMOSTRAS SELECIONADAS PARA TREINAMENTO")
            print("-" * 90)
            print(f"Total selecionado: {len(selected_df)}")
            print(f"\nDistribuição por espessura:")
            print(selected_df['espessura_chapa'].value_counts().sort_index().to_string())
            print(f"\nDistribuição por num. parafusos:")
            print(selected_df['num_parafusos'].value_counts().sort_index().to_string())
            print()
        
        print("="*90)

