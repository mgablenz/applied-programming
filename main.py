import leafmap
import pandas as pd
import os
import data_curation

m = leafmap.Map(center=(47.0, 8.0), zoom=7)

df = swiss_population_df

births = df.dropna(subset=["birth_lat", "birth_lon"])
deaths = df.dropna(subset=["death_lat", "death_lon"])

m.add_circle_markers_from_xy(births, x="birth_lon", y="birth_lat", radius=5,
                             color="blue", fill_color="blue", fill_opacity=0.5,
                             popup=["birthPlaceLabel"])

m.add_circle_markers_from_xy(deaths, x="death_lon", y="death_lat", radius=5,
                             color="red", fill_color="red", fill_opacity=0.5,
                             popup=["deathPlaceLabel"])

m.save("map.html")