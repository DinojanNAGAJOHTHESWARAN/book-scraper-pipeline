import pandas as pd
from datetime import datetime
import os

def clean_data(data):
    df = pd.DataFrame(data)


    try:
        df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    except Exception as e:
        print(f"[ERREUR] Conversion du prix: {e}")
        df["price"] = pd.NA


    rating_map = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    df["rating"] = df["rating"].map(rating_map).fillna(0).astype(int)


    df["date"] = datetime.today().strftime("%Y-%m-%d")


    df = df[["date","title","category","price","rating"]]

    return df

def save_csv(df, path):
    try:
   
        os.makedirs(os.path.dirname(path), exist_ok=True)

  
        df.to_csv(path, index=False, mode='a', header=not os.path.exists(path))
        print(f"[INFO] CSV mis à jour : {path}")
    except Exception as e:
        print(f"[ERREUR] Impossible de sauvegarder CSV: {e}")