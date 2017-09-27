import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster.bicluster import SpectralCoclustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def time_series(df):
    sns.set(style='dark')
    varlist = df.columns.drop(['asset', 'unixtime'])
    df = df[df['unixtime'].isin(df['unixtime'].unique()[::10])]

    fig, axs = plt.subplots(14, 2, figsize=(10, 15), sharex=True)
    for ax, n in zip(axs.flat, range(len(varlist))):
        subset = df.melt(id_vars=['asset', 'unixtime'],
                         value_vars=varlist[n])
        bot = subset['value'].min()
        top = subset['value'].max()
        sns.tsplot(data=subset, time='unixtime', value='value', unit='asset',
                   condition='variable', ax=ax, err_style='unit_traces',
                   color=sns.hls_palette(len(varlist) + 1, l=.5, s=.5)[n])
        ax.set(xticks=(), yticks=(bot, top), ylabel='', xlabel='')
        ax.set_yticklabels(np.round([bot, top], 2), fontsize=8)
        ax.set_title(varlist[n], fontweight='bold', fontsize=9)
        ax.legend_ = None

    sns.despine(left=True, bottom=True)
    fig.suptitle(f'Variable Time Series', fontsize=20)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig('reports/time_series.png')


def distributions(df):
    sns.set(style='darkgrid')
    varlist = df.columns.drop(['asset', 'unixtime'])

    fig, axs = plt.subplots(7, 4, figsize=(10, 10))
    for ax, n in zip(axs.flat, range(len(varlist))):
        subset = df[varlist[n]]
        bot = subset.min()
        top = subset.max()
        sns.violinplot(data=subset.values, ax=ax, linewidth=.8, bw=.1,
                       color=sns.hls_palette(len(varlist) + 1, l=.7, s=.5)[n])
        ax.set(xticks=(), yticks=(bot, np.mean([bot, top]), top))
        ax.set_yticklabels([np.round(bot, 2), '', np.round(top, 2)],
                           fontsize=8)
        ax.set_title(varlist[n], fontweight='bold', fontsize=9)

    sns.despine(left=True, bottom=True)
    fig.suptitle(f'Variable Distributions', fontsize=20)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig('reports/distributions.png')


def principal_components(df):
    sns.set(style='white', font_scale=.9)
    comps = 6
    asset_list = df['asset'].unique()
    scaled = StandardScaler().fit_transform(df.drop(['asset', 'unixtime'],
                                                    axis=1))
    reduced = PCA(n_components=comps).fit_transform(scaled)

    grid_rows = int(np.ceil(np.sqrt(comps)))
    grid_cols = int(np.ceil(comps / grid_rows))
    fig, axs = plt.subplots(grid_rows, grid_cols, figsize=(10, 10))
    for ax in axs.flat[comps:]:
        ax.axis('off')
    for c, s in zip(range(comps), np.linspace(0, 3, comps + 1)):
        ax = axs.flat[c]
        pal = sns.cubehelix_palette(start=s, light=.6, n_colors=5)
        for asset in asset_list:
            sns.kdeplot(reduced[:, c][df['asset'] == asset], ax=ax,
                        shade=True, label=asset, color=pal.pop(0), cut=0)
        ax.legend(title=f'Component {c+1}')

    fig.suptitle('Principal Component Distribution by Asset',
                 fontsize=20)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig('reports/principal_components.png')


def top_correlations(df):
    sns.set(style='white', font_scale=.9)
    pearson = df.drop(['asset', 'unixtime'], axis=1).corr(method='pearson')
    pairs = pearson.where(np.triu(np.ones(pearson.shape, dtype='bool'),
                                  k=1)).stack().sort_values(ascending=False)

    grid = dict(height_ratios=[1, .5])
    fig, axs = plt.subplots(2, 1, figsize=(7, 10), gridspec_kw=grid)

    subset = pairs[pairs >= 0].head(30)
    sns.barplot(x=subset.values, y=subset.index, ax=axs[0],
                palette=sns.color_palette('OrRd_r', 30))
    axs[0].set(xlim=(.5, 1), xticks=(),
               yticklabels=[v[0] + ' - ' + v[1] for v in subset.index])
    axs[0].set_yticklabels([v[0] + ' - ' + v[1] for v in subset.index])
    for i, corr in zip(range(len(subset)), subset.values):
        axs[0].text(corr + .01, i, round(corr, 2), va='center')

    subset = pairs[pairs < 0].tail(15)
    sns.barplot(x=subset.values, y=subset.index, ax=axs[1],
                palette=sns.color_palette('PuBu', 15))
    axs[1].set(xlim=(-.5, -1), xticks=(),
               yticklabels=[v[0] + ' - ' + v[1] for v in subset.index])
    for i, corr in zip(range(len(subset)), subset.values):
        axs[1].text(corr - .01, i, round(corr, 2), va='center')

    sns.despine(bottom=True)
    fig.suptitle(f'Top Variable Correlation Pairs', fontsize=20)
    fig.tight_layout(rect=(0, 0, .95, .95))
    fig.savefig('reports/top_correlations.png')


def correlation_matrix(df):
    sns.set(style='white', font_scale=.9)
    clusters = 4
    pearson = df.drop(['asset', 'unixtime'], axis=1).corr(method='pearson')
    clust = SpectralCoclustering(n_clusters=clusters, random_state=0)
    clust.fit(pearson)
    pearson = pearson.iloc[np.argsort(clust.row_labels_)[::-1],
                           np.argsort(clust.column_labels_)]

    grid = dict(width_ratios=[1.5, pearson.shape[1]])
    fig, axs = plt.subplots(1, 2, figsize=(10, 8), gridspec_kw=grid)

    sns.heatmap(data=np.sort(clust.row_labels_)[::-1].reshape(-1, 1),
                ax=axs[0],
                cbar=False, linewidths=.005,
                cmap=sns.color_palette('Spectral'))
    axs[0].set(xticks=(), yticks=())

    sns.heatmap(data=pearson,
                cmap=sns.diverging_palette(220, 10, n=11),
                linewidths=.005,
                cbar_kws={'shrink': .75}, vmax=1, vmin=-1,
                ax=axs[1])
    axs[1].set_xticklabels(pearson.columns, rotation='vertical')
    axs[1].set_yticklabels(pearson.index, rotation='horizontal')

    fig.suptitle(f'Variable Correlation Matrix in {clusters} Clusters',
                 fontsize=20)
    fig.tight_layout(w_pad=.5, rect=(.03, 0, 1, .95))
    fig.savefig('reports/correlation_matrix.png')


data = pd.read_csv('processed/2015-05.csv.gz', compression='gzip').dropna()

time_series(data)
distributions(data)
principal_components(data)
correlation_matrix(data)
top_correlations(data)
