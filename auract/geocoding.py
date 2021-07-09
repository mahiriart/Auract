"""This module contain geocoding function to find latitude and longitude base on a zip-code. Local data-bank in
/Geocoding/geodata/allclean.csv """
import re
import os
import pandas as pd
from .log import log
from .settings import data_dir, geo_csv_ll_dir

df_geo = pd.read_csv(os.path.join(data_dir, 'geodata/allclean.csv'))


def latfinder(zipdf):
    if not re.match('[0-9]', str(zipdf)):
        log("\t Warning- zip code : " + str(zipdf) + " is not valid must match regex [0-9] location node will be ignored",
            type='warning')
        log()
        return
    string = str(re.sub("[][]", '', str(df_geo.lat.loc[df_geo['zip_code'] == float(zipdf)].head(1).values)))
    if string:
        return string
    else:
        reducezip = (re.sub(".{2}$", '00', str(zipdf)))
        log("\t latlong not found for zip-code: " + str(zipdf) + " trying with reduced zip-code " + reducezip,
            type='info')
        string = str(re.sub("[][]", '', str(df_geo.lat.loc[df_geo['zip_code'] == float(reducezip)].head(1).values)))

        if string:
            log("\t\t success", type='info')
            return string
        else:
            log("\t latlong can't be found for " + str(zipdf) + " even with reduced zip-code", type='info')


def longfinder(zipdf):
    if not re.match('[0-9]', str(zipdf)):
        return
    string = str(re.sub("[][]", '', str(df_geo.long.loc[df_geo['zip_code'] == float(zipdf)].head(1).values)))
    if string:
        return string
    else:
        reducezip = (re.sub(".{2}$", '00', str(zipdf)))
        string = str(re.sub("[][]", '', str(df_geo.long.loc[df_geo['zip_code'] == float(reducezip)].head(1).values)))
        if string:
            return string


def geocoding(csv_path):
    df = pd.read_csv(csv_path)
    for col in df.columns:
        if col.lower() in ('zip-code', 'zip_code', 'zipcode', 'zip code'):
            df.rename(columns={col: 'zip-code'}, inplace=True)
            break
    else:
        log("zip-code collum is missing geocoding process stop", type="warning")
        return csv_path

    log("Finding latlong for all zip-code: ", type="info")
    log()
    df['latitude'] = df.apply(lambda row: latfinder(row['zip-code']), axis=1)

    df['longitude'] = df.apply(lambda row: longfinder(row['zip-code']), axis=1)

    if not os.path.exists(geo_csv_ll_dir):
        os.makedirs(geo_csv_ll_dir)
    csv_path = os.path.join(geo_csv_ll_dir, os.path.splitext(os.path.basename(csv_path))[0] + ".csv")
    df.to_csv(csv_path, index=False)
    return csv_path

