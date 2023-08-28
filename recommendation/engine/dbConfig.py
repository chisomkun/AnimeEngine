import sqlite3 
import pandas as pd

conn = sqlite3.connect("db.sqlite3")

def animeConnect():
    select = pd.read_sql_query("SELECT * FROM anime",conn)
    anime_df = pd.DataFrame(select, columns=['anime_id','name','genre','type','episodes','rating','members'])
    return anime_df

def ratingConnect():
    select = pd.read_sql_query("SELECT * FROM rating",conn)
    rating_df = pd.DataFrame(select, columns=['user_id','anime_id','rating'])
    return rating_df