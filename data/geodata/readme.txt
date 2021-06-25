All data comes from www.geonames.org

Own data:
To use your own geocoding database:
    use a csv file with this header: lat,long,zip-code
       and replace allclean.csv

Add data:
If you want to add more data to the current database open allclean.csv and add it at the end of the file with the same column order.

Where to get data:
    I recommend using data from www.geonames.org i had a 95% correspondence with 500zip-code from france.

    Quick example:
    download .txt file you want convert it to csv and extract the 3needed column :'zip-code' 'latitude' and 'longitude' with pandas dataframe

    Here a function example to get 'zip-code' 'latitude' and 'longitude' from .csv note that you need to find the column first and adapt 'usecols=[]'' because it might change between each .txt file:
        # reunion
        def re_clean():
            df_geo_re = pd.read_csv('./data/csv/re.csv', delimiter="\t",
                                    header=None, usecols=[4, 5, 13], names=['lat', 'long', 'zip_code'])
            df_geo_re = df_geo_re.dropna()
            df_geo_re.to_csv('./data/clean/reclean.csv', index=False)


allclean.csv info:
current database used:
    FR
    RE
    MQ
    GP
    NC
    YT
    laposte.fr //a lots redundant data with other but allows me to get a bit more correspondence

line manually added:
lat,long,zip-code
-22.26667,166.46667, 98800.0
