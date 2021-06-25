"""
This module contain function to add a color gradient based on matrix given
"""
import pandas as pd

def min_distance_value(matricepath):
    df = pd.read_csv(matricepath, sep="\t", index_col=0)
    df_color = pd.DataFrame(columns=['id', 'min_value_compare_to_other', 'min_value_compare_to_other__colour'], index= None)
    dico = df.to_dict()
    for key, val in dico.items():
        min = None
        for key2, val2 in val.items():
            if not min:
                min = val2
            if key2 != key and val2 <= min:
                min = val2
        df_color = df_color.append({'id': key, 'min_value_compare_to_other': str(min), 'min_value_compare_to_other__colour': hexvalue(min)}, ignore_index=True)
    return df_color

def hexvalue(min):
    if min <= 30:
        if min <= 20:
            if min <= 10:
                return "#ff0000"
            return "#ffaa00"
        return "#ffff00"
    else:
        return "#ffffff"