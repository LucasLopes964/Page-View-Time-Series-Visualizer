import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Corrigir depreciação np.float em versões novas do numpy
if not hasattr(np, 'float'):
    np.float = float

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# ========================================
# 1. LINE PLOT
# ========================================
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig('line_plot.png')
    return fig

# ========================================
# 2. BAR PLOT   <<--- AQUI FICA O draw_bar_plot
# ========================================
def draw_bar_plot():
    # Preparar dados
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupar por ano/mês e calcular média
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Plotar
    fig = df_grouped.plot(kind='bar', figsize=(10, 8)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(
        title="Months",
        labels=[calendar.month_name[i] for i in range(1, 13)]  # <<-- meses completos
    )

    fig.savefig('bar_plot.png')
    return fig

# ========================================
# 3. BOX PLOT
# ========================================
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Year-wise
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise
    sns.boxplot(
        x="month", y="value", data=df_box, ax=axes[1],
        order=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig