All data comes from www.geonames.org and laposte.fr

Use own data:
To use your own geocoding database:
    use a csv file with this header: lat,long,zip-code
       and replace allclean.csv

Add data:
If you want to add more data to the current database open allclean.csv and add it at the end of the file with the same column order.

Where to get data:
    I recommend using data from www.geonames.org i had a 95% correspondence with 500 test zip-code from france.

    Quick example:
    Download the .txt file you want at www.geonames.org, convert it to csv and extract the 3needed column :'zip-code' 'latitude' and 'longitude' with pandas dataframe

    Here a function example to extract this 'zip-code' 'latitude' and 'longitude' column from .csv.
    Important, first you will need to find each column index and adapt 'usecols=[x, y, z]'' because it might change between each .txt file.
    Here an example for the RE.txt file:
        # reunion
        def re_clean():
            df_geo_re = pd.read_csv('./data/csv/re.csv', delimiter="\t",
                                    header=None, usecols=[4, 5, 13], names=['lat', 'long', 'zip_code'])
            df_geo_re = df_geo_re.dropna()
            df_geo_re.to_csv('./data/clean/reclean.csv', index=False)


    Then add the new csv data at the end of allclean.csv


allclean.csv info:
    current file used:
        FR
        RE
        MQ
        GP
        NC
        YT
        laposte.fr //a lots of redundant data with other but allows me to get a better result

    line manually added:
    lat,long,zip-code
    -22.26667,166.46667, 98800.0
