import pandas as pd

def sampleKRows(k=5528):
    data = pd.read_csv('data/warfarin.csv', header=0)
    data = data.dropna(axis=0, subset=['Therapeutic Dose of Warfarin'])
    return data.sample(k, replace = False)
