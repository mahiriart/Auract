"""
This module contain function to add a color gradient based on matrix given
"""
import pandas as pd


def min_distance_value(matricepath):
    df = pd.read_csv(matricepath, sep="\t", index_col=0)
    df_color = pd.DataFrame({'id': pd.Series([], dtype='int'),
                             'min_value_compare_to_other': pd.Series([], dtype='int'),
                             'min_value_compare_to_other__colour': pd.Series([], dtype='str')}, index=None)
    dico = df.to_dict()
    for key, val in dico.items():
        min = None
        for key2, val2 in val.items():
            if not min:
                min = val2
            if str(key2) != str(key) and int(val2) <= int(min):
                min = val2
        df_color = df_color.append(
            {'id': key, 'min_value_compare_to_other': int(min),
             'min_value_compare_to_other__colour': str(hexvalue(min))},
            ignore_index=True)
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
