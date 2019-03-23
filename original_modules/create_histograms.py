
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from create_dataframes import create_df, prepare_df 

def create_histogram(df2, keyword):
    #Word Count for Lit
    df3=df2[df2['Keyword']== keyword]
    df3=df3.groupby(['State'])[['Word Count']].sum().reset_index()
    df3.hist()
    df3.set_index('State')[['Word Count']].plot.bar(figsize=(20, 5))
    plt.title('Words Count For "'+ keyword +'" Word')
    plt.ylabel('Words Count')
    plt.savefig(keyword + '.png')


