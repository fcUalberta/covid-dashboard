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
    # X1= scipy.sparse.load_npz(os.path.join(path,'X1.npz'))
    df_covid = pd.read_pickle(os.path.join(path,'df_covid'))
    return df_covid

def scatter_data(k):
    filename = "X_embedded_child"+str(k)+".npy"
    X_embedded_child5 = np.load(os.path.join(path,filename),allow_pickle= True)
    return X_embedded_child5

def sunburst_single(k):
    filename = "y_pred"+str(k)+".npy"
    y_pred5=np.load(os.path.join(path,filename),allow_pickle= True)
    return y_pred5

def sunburst_multi(k):
    child = []
    for i in range(1,6):
        filename = 'y_pred_child'+str(k)+'-'+str(i)+'.npy'
        child.append(np.load(os.path.join(path,filename)))
        # print(np.array(child).shape)
    return child
# sunburst_multi(10)
