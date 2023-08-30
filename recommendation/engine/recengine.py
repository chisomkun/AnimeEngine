import scipy as sp
import numpy as np
import warnings
import pandas as pd
import sklearn as sklearn
import sqlite3 
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

pd.options.display.max_columns

conn = sqlite3.connect("db.sqlite3")
select = pd.read_sql_query("SELECT * FROM anime",conn)
anime_df = pd.DataFrame(select, columns=['anime_id','name','genre','type','episodes','rating','members'])
select1 = pd.read_sql_query("SELECT * FROM rating",conn)
rating_df = pd.DataFrame(select1, columns=['user_id','anime_id','rating'])

#warning hadle
warnings.filterwarnings("always")
warnings.filterwarnings("ignore")

#Engineer dataframe: only recommend TV animes, only computing first 7500 users TODO increase users
rated_anime = rating_df.merge(anime_df, left_on = 'anime_id', right_on = 'anime_id', suffixes= ['_user', ''])
rated_anime =rated_anime[['user_id', 'name', 'rating']]
rated_anime_7500= rated_anime[rated_anime.user_id <= 7500]

#Cosine Similarity model
pivot = rated_anime_7500.pivot_table(index=['user_id'], columns=['name'], values='rating')

#Engineer Pivot table: Normalize Values, fill NaN w/ 0s,
#Transposing pivot table, dropping col w/ 0, scipy used to convert sparse matrix format for similiarity computation
pivot_n = pivot.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1)
pivot_n.fillna(0, inplace=True)
pivot_n = pivot_n.T
pivot_n = pivot_n.loc[:, (pivot_n != 0).any(axis=0)]
piv_sparse = sp.sparse.csr_matrix(pivot_n.values)

#model based on anime similarity
anime_similarity = cosine_similarity(piv_sparse)

#Df of anime similarities
ani_sim_df = pd.DataFrame(anime_similarity, index = pivot_n.index, columns = pivot_n.index)

def anime_recommendation(ani_name):
    rec = []
    moreRec = []
    
    number = 1 
    number1 = 6
    for anime in ani_sim_df.sort_values(by = ani_name, ascending = False).index[1:6]:
        rec.append(f"#{number}:{anime}, {round(ani_sim_df[anime][ani_name]*100,2)}% match")
        number +=1 

    for anime in ani_sim_df.sort_values(by = ani_name, ascending = False).index[6:11]:
        moreRec.append(f"#{number1}:{anime}, {round(ani_sim_df[anime][ani_name]*100,2)}% match")
        number1 +=1 
    
    return rec , moreRec
