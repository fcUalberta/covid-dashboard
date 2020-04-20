"""
Module to preprocess the COVID Research Database
"""
# Importing libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.manifold import TSNE
from sklearn.cluster import MiniBatchKMeans
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from plotly.offline import plot
import plotly.graph_objects as go
import numpy as np
import statistics
import re
import scipy.sparse
from sklearn.manifold import TSNE

# Reading in the unprocessed dataframe data
df_covid = pd.read_pickle(r'cluster_data\df_covid')
df = pd.read_pickle(r'cluster_data\df_covid')

# Adding columns for word count in abstract and body
df_covid['abstract_word_count'] = df_covid['abstract'].apply(lambda x: len(x.strip().split()))
df_covid['body_word_count'] = df_covid['body_text'].apply(lambda x: len(x.strip().split()))


df_covid.info()

# Printing abstract column description to see if there are any anomalies
df_covid['abstract'].describe(include='all')

# Droppping duplicates
df_covid.drop_duplicates(['abstract', 'body_text'], inplace=True)

# Dropping nan values
df_covid.dropna(inplace=True)

# Validating after dropping
print(df_covid.info())

# Selecting 20000 articles only for efficiency in visualization
df_covid = df_covid.head(20000)

# Removing punctuation from each both abstract and body text
df_covid['body_text'] = df_covid['body_text'].apply(lambda x: re.sub('[^a-zA-z0-9\s]','',x))
df_covid['abstract'] = df_covid['abstract'].apply(lambda x: re.sub('[^a-zA-z0-9\s]','',x))
#make all word lower case
def lower_case(input_str):
    """
    Function to convert the input string to lower case..
    """
    input_str = input_str.lower()
    return input_str

# Converting both astract and body to lower case
df_covid['body_text'] = df_covid['body_text'].apply(lambda x: lower_case(x))
df_covid['abstract'] = df_covid['abstract'].apply(lambda x: lower_case(x))

# Dropping unnecessary columns
text = df_covid.drop(["paper_id", "abstract", "abstract_word_count", "body_word_count",
                      "authors", "title", "journal", "abstract_summary"], axis=1)

# DataFrame into 1D list where each index is an article (instance)
text_arr = text.stack().tolist()

# Creating 2D list
words = []
for ii in range(0,len(text)):
    words.append(str(text.iloc[ii]['body_text']).split(" "))
print(words[0][:10])

# Creating the n-grams for text co occurence
n_gram_all = []
for word in words:
    # get n-grams for the instance
    n_gram = []
    for i in range(len(word)-2+1):
        n_gram.append("".join(word[i:i+2]))
    n_gram_all.append(n_gram)

# Initializing hash vectorizer
hvec = HashingVectorizer(lowercase=False, analyzer=lambda l:l, n_features=2**10)
# Creating features matrix X1
X1 = hvec.fit_transform(n_gram_all)

# Saving the feature matrix output
scipy.sparse.save_npz(r'cluster_data\X1', X1)
sparse_matrix = scipy.sparse.load_npz(r'cluster_data\X1.npz')

# Loading the file
d = np.load(r'cluster_data\X1.npy',allow_pickle=True)

# Applying TSNE
X_embedded2 = TSNE(n_components=2).fit_transform(X1)
pd.DataFrame(X_embedded2).to_csv(r"cluster_data\X_embedded2.csv", index=None)
data = pd.read_csv(r"cluster_data\X_embedded2.csv")
data = np.array(data,dtype=float32)
