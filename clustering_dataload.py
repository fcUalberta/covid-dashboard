"""
Module for loading the cluster input data from numpy arrays
"""
import numpy as np
import pandas as pd
import scipy.sparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.cluster import MiniBatchKMeans
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from plotly.offline import plot
import plotly.graph_objects as go
import numpy as np
import statistics


path = r"cluster_data/"

def initial_data():
    """
    Function to load the DataFrame of pre-processed Research Database

    Returns:
    Dataframe of pre-processed Research database
    """
    df_covid = pd.read_pickle(os.path.join(path,'df_covid'))
    return df_covid

def scatter_data(k):
    """
    Function to load single level clustering input from numpy arrays

    Args:

    k: The number of clusters needed

    Returns:
    A numpy array with required number of clusters
    """
    filename = "X_embedded_child"+str(k)+".npy"
    X_embedded_child = np.load(os.path.join(path,filename),allow_pickle= True)
    return X_embedded_child

def sunburst_single(k):
    """
    Function to load first level of cluster input from numpy arrays for sunburst

    Args:
    k: The number of clusters needed

    Returns:
    A numpy array with required number of parent clusters for sunburst and dendrogram
    """
    filename = "y_pred"+str(k)+".npy"
    y_pred5=np.load(os.path.join(path,filename),allow_pickle= True)
    return y_pred5

def sunburst_multi(k):
    """
    Function to load second level of cluster input from numpy arrays for sunburst

    Args:
    k: The number of child clusters needed  for second level

    Returns:
    A numpy array with required number of child clusters for sunburst and dendrogram
    """
    child = []
    for i in range(1,6):
        filename = 'y_pred_child'+str(k)+'-'+str(i)+'.npy'
        child.append(np.load(os.path.join(path,filename)))
        # print(np.array(child).shape)
    return child
# sunburst_multi(10)
