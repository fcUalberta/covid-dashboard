# -*- coding: utf-8 -*-
"""
Module to apply Clustering on Pre-preprocessed COVID research dataset
and save the clusters as numpy arrays which are used for visualization
"""

# Importing libraries
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
import numpy as np
import pandas as pd
import scipy.sparse

# Loading the preprocessed files
X_embedded2 = pd.read_csv(r"cluster_data\X_embedded2.csv")
X_embedded2=np.array(X_embedded2,dtype='float32')
X1= scipy.sparse.load_npz(r'cluster_data\X1.npz')
df_covid = pd.read_pickle(r'cluster_data\df_covid')

# Running K-Means for single level clustering
k=5
if k == 5:
    kmeans = MiniBatchKMeans(n_clusters=k)
    y_pred5 = kmeans.fit_predict(X1)
    X_embedded_child5=[[] for _ in range(k)]
    for i in range(len(X_embedded2)):
        for ii in range(0,k):
            if y_pred5[i]== ii :
                (X_embedded_child5[ii]).append(X_embedded2[i])

# Saving the files for single level clustering for different number of clusters

if k==5:
    pd.DataFrame(X_embedded_child5).to_csv(r"cluster_data\X_embedded_child5.csv", index=None)
    np.save(r'cluster_data\y_pred5',y_pred5)
elif k==10:
    pd.DataFrame(X_embedded_child5).to_csv(r"cluster_data\X_embedded_child10.csv", index=None)
    np.save(r'cluster_data\y_pred10',y_pred5)
else:
    pd.DataFrame(X_embedded_child5).to_csv(r"cluster_data\X_embedded_child15.csv", index=None)
    np.save(r'cluster_data\y_pred15',y_pred5)

# Runnin K means for the children of first level clusters for multi-level
# Clustering. The values of k2 is changed from 5 to 10 to get
# 5-Parent 5 Child or 5-Parent 10 Child clusters
k2=5
n=-5
if k2 == 5 :
    Y_child=[[] for _ in range(k)]
    y_pred_child=[[] for _ in range(k)]
    kmeans = MiniBatchKMeans(n_clusters=k2)
    X_embedded_child_child=[[] for _ in range(k2*k)]
    for i in range (0,k) :
        if len (X_embedded_child5[i]) > 5 :
            y_pred_child[i]=(kmeans.fit_predict(X_embedded_child5[i]))
            n=n+5
            for ii in range(0,(len( y_pred_child[i]))) :
                for iii in range (0,k2):
                    if y_pred_child[i][ii]==iii:
                        m=iii+n
                        (X_embedded_child_child[m]).append(X_embedded_child5[i][ii])
        else:
            n=n+5
            for ii in range(0,(len( y_pred_child[i]))) :
                for iii in range (0,k2):
                    if y_pred_child[i][ii]==iii:
                        m=iii+n
                        (X_embedded_child_child[m]).append(X_embedded_child5[i][ii])

# Saving all the npy files for child clusters for each parent.
np.save(r'cluster_data\y_pred_child[0]',y_pred_child[0])
np.save(r'cluster_data\y_pred_child[1]',y_pred_child[1])
np.save(r'cluster_data\y_pred_child[2]',y_pred_child[2])
np.save(r'cluster_data\y_pred_child[3]',y_pred_child[3])
np.save(r'cluster_data\y_pred_child[4]',y_pred_child[4])
