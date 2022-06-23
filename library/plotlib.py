import enum
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from typing import Optional, List, Dict, Tuple
from math import sqrt, ceil


def draw_stacked_bar_subplots(data: pd.DataFrame, x: List[str], y: str, colors: List[str],
                    figsize: Optional[Tuple[int,int]]=None, shape: Optional[Tuple[int,int]]=None,
                    total: Optional[bool]=True, xbins: Optional[Dict[str,int]]=dict(), ybins: Optional[int]=0,
                    normalize: Optional[bool]=True, labels: Optional[Dict[any,any]]=None, reversed: Optional[bool]=False,
                    title: Optional[str]=None, titlesize: Optional[int]=18, subtitle: Optional[bool]=True, subtitlesize: Optional[int]=14,
                    names: Optional[Dict[any,str]]=None, annot: Optional[bool]=True, annotsize: Optional[int]=9, **kwargs) -> Tuple[Figure,np.ndarray]:
    """
    draw subplots of stacked bar groupby x.
    if the feature is numerical, set bins.
    if you want to change x and y position, set reversed true.
    """

    kwargs = locals()
    nrows = shape[0] if shape else ceil(sqrt(len(x)))
    ncols = shape[1] if shape else ceil(len(x)/nrows)
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize)

    features = np.pad(x, (0,ncols*nrows-len(x)), constant_values=str())
    features_2d = np.resize(features, (nrows,ncols))
    kwargs['title'] = 'default' if subtitle else None
    kwargs['titlesize'] = subtitlesize

    for row, features in enumerate(features_2d):
        for col, x in enumerate(features):
            if x == str():
                break
            kwargs['ax'] = ax[row,col] if nrows > 1 else ax[col]
            if reversed:
                kwargs.update({'x':y,'y':x,'xbins':ybins,'ybins':xbins.get(x,0)})
                kwargs.update({'xlabels':labels.get(y),'ylabels':labels.get(x)})
            else:
                kwargs.update({'x':x,'y':y,'xbins':xbins.get(x,0),'ybins':ybins})
                kwargs.update({'xlabels':labels.get(x),'ylabels':labels.get(y)})
            draw_stacked_bar(**kwargs)

    fig.suptitle(title, fontsize=titlesize)
    return fig, ax


def draw_stacked_bar(data: pd.DataFrame, x: str, y: str, ax: Figure, colors: List[str], total: Optional[bool]=True,
                    xbins: Optional[int]=0, ybins: Optional[int]=0, normalize: Optional[bool]=True,
                    xlabels: Optional[Dict[any,any]]=None, ylabels: Optional[Dict[any,any]]=None,
                    title: Optional[str]=None, titlesize: Optional[int]=16, names: Optional[Dict[any,str]]=None,
                    nlegend: Optional[int]=3, annot: Optional[bool]=True, annotsize: Optional[int]=9, **kwargs):
    """
    draw stacked bar groupby x.
    if the feature is numerical, set bins.
    """

    range_df = groupby_range(**locals())
    range_df = range_df.reset_index().rename(columns={'index':x})

    if title == 'default':
        title = f'{names[y]} by {names[x]}'
    yticks = [0.0,0.2,0.4,0.6,0.8,1.0,1.2]
    plot = range_df.plot.bar(ax=ax, x=x, stacked=True, color=colors, yticks=yticks, rot=0)
    plot.set_title(title, fontsize=titlesize)
    plot.legend(loc='upper center', ncol=nlegend, fancybox=True, shadow=True)

    if annot:
        display_plot_values(plot, normalize, fontsize=annotsize)
        plot.get_yaxis().set_visible(False)
        plot.set_xticklabels(list(range_df[x].unique()))


def groupby_range(data: pd.DataFrame, x: str, y: str, total: Optional[bool]=True,
                xbins: Optional[int]=0, ybins: Optional[int]=0, normalize: Optional[bool]=True,
                xlabels: Optional[Dict[any,any]]=None, ylabels: Optional[Dict[any,any]]=None, **kwargs) -> pd.DataFrame:
    """
    make table groupby x.
    if the feature is numerical, set bins.
    """

    data = data.copy()

    for target, bins, labels in zip([x,y],[xbins,ybins],[xlabels,ylabels]):
        if bins > 0:
            data[target] = pd.cut(data[target], bins=bins, precision=0)
            data[target] = data[target].apply(lambda s: str(s).replace('.0',''))
        if labels:
            data[target] = data[target].apply(lambda s: labels[s])

    xlabels =  list(xlabels.values()) if xlabels else sorted(data[x].unique())
    ylabels = list(ylabels.values()) if ylabels else sorted(data[y].unique())
    data[y] = data[y].apply(lambda s: ylabels.index(s))

    range_df = [data[y].value_counts(normalize=normalize).sort_index()] if total else list()
    range_df += [data[data[x]==r][y].value_counts(normalize=normalize).sort_index() for r in xlabels]
    range_df = pd.DataFrame(range_df).fillna(0)
    range_df.columns = ylabels
    range_df.index = ['Total']+xlabels if total else xlabels

    return range_df


def display_plot_values(plot: any, normalize: Optional[bool]=True, fontsize: Optional[int]=9, **kwargs):
    """
    display values on each plot patch.
    """

    plot.xaxis.set_major_formatter(PercentFormatter(1))
    for p in plot.patches:
        h, w, x, y = p.get_height(), p.get_width(), p.get_x(), p.get_y()
        if h > 0.0:
            text = f'{h * 100:0.2f} %' if normalize else f'{h:0.0f}'
            plot.annotate(text=text, xy=(x+w/2,y+h/2), ha='center', va='center', fontsize=fontsize)
