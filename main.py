import leafmap
import pandas as pd
import os
from data_curation import df
from geopy.distance import geodesic

cols = ["birth_lat", "birth_lon", "death_lat", "death_lon"]
df["distance_km"] = df.apply(
    lambda r: geodesic((r["birth_lat"], r["birth_lon"]), (r["death_lat"], r["death_lon"])).km
    if r[cols].notna().all() else float("nan"),
    axis=1,
)

df.to_excel("with_distance.xlsx")
print(df["distance_km"].mean())

m = leafmap.Map(center=(47.0, 8.0), zoom=7)


births = df.dropna(subset=["birth_lat", "birth_lon"])
deaths = df.dropna(subset=["death_lat", "death_lon"])

m.add_circle_markers_from_xy(births, x="birth_lon", y="birth_lat", radius=5,
                             color="blue", fill_color="blue", fill_opacity=0.5,
                             popup=["birthPlaceLabel"])

m.add_circle_markers_from_xy(deaths, x="death_lon", y="death_lat", radius=5,
                             color="red", fill_color="red", fill_opacity=0.5,
                             popup=["deathPlaceLabel"])

m.save("map.html")