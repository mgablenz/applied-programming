import os
import csv
import pandas as pd
import openpyxl
import leafmap
import webbrowser

swiss_population_df = pd.read_csv(os.path.join('data', 'swiss-people-wikipedia-2.csv'))

cols = ["geonameid", "name", "asciiname", "alternatenames", "lat", "lon",
        "fclass", "fcode", "country", "cc2", "admin1", "admin2", "admin3",
        "admin4", "population", "elevation", "dem", "tz", "modified"]

def load_gn(country):
    gn = pd.read_csv(os.path.join('data', f"{country}.txt"), sep="\t", names=cols,
                     quoting=csv.QUOTE_NONE,
                     usecols=["name", "lat", "lon", "fclass", "population"])
    # populated places only, largest first within the country
    return gn[gn.fclass == "P"].sort_values("population", ascending=False)

# CH first: on a name clash, the Swiss place wins; then the largest within the country
gn = (pd.concat([load_gn("CH"), load_gn("DE"), load_gn("IT"), load_gn("GB"), load_gn("FR"), load_gn("US"), load_gn("NL"), load_gn("AT"), load_gn("CH")])
        .drop_duplicates("name", keep="first")
        .set_index("name"))

for p in ["birth", "death"]:
    swiss_population_df[f"{p}_lat"] = swiss_population_df[f"{p}PlaceLabel"].map(gn["lat"])
    swiss_population_df[f"{p}_lon"] = swiss_population_df[f"{p}PlaceLabel"].map(gn["lon"])

# unmatched names
df = swiss_population_df
miss = pd.concat([df.loc[df.birth_lat.isna(), "birthPlaceLabel"],
                  df.loc[df.death_lat.isna(), "deathPlaceLabel"]]).dropna().unique()

df = swiss_population_df

death_miss = df[df.deathPlaceLabel.notna() & df.death_lat.isna()]

# all affected rows (every column), tab-separated
death_miss.to_csv("death_misses.txt", sep="\t", index=False, encoding="utf-8")

# optionally also just the unique place names with counts
death_miss.deathPlaceLabel.value_counts().to_csv(
    "death_miss_names.txt", sep="\t", header=False, encoding="utf-8")

#print(len(death_miss), "rows,", death_miss.deathPlaceLabel.nunique(), "unique places")
df.to_excel("output.xlsx")
print