import xarray as xr
import json

# Load the dataset
data = xr.open_dataset("./puget_sound_data/wod_ctd_2021.nc")
print("Dataset loaded.")

# Debugging: Print dataset summary
print(data)

# Verify available dimensions and coordinates
print(f"Available dimensions: {list(data.dims)}")
print(f"Available coordinates: {list(data.coords)}")

# Extract temperature and salinity at the surface level
try:
    temperature = data["Temperature"].isel(Temperature_obs=0).values  # Assuming surface-level data
    salinity = data["Salinity"].isel(Salinity_obs=0).values  # Assuming surface-level data
    latitudes = data["lat"].values
    longitudes = data["lon"].values
    print("Variables extracted: Temperature, Salinity, Latitude, Longitude.")
except KeyError as e:
    raise KeyError(f"Required variable missing: {e}")

# Convert to GeoJSON format
features = []
for i in range(len(latitudes)):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(longitudes[i]), float(latitudes[i])]
        },
        "properties": {
            "Temperature": float(temperature[i]),
            "Salinity": float(salinity[i]),
        }
    }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Save to GeoJSON file
geojson_file_path = "./puget_sound_data/puget_sound_data.geojson"
with open(geojson_file_path, "w") as f:
    json.dump(geojson_data, f, indent=2)
    print(f"GeoJSON file saved: {geojson_file_path}")
