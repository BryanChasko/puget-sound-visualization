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

# Extract surface-level temperature and salinity
try:
    temperature = data["Temperature"].isel(Temperature_obs=0).values.flatten()  # Flatten array to 1D
    salinity = data["Salinity"].isel(Salinity_obs=0).values.flatten()  # Flatten array to 1D
    latitudes = data["lat"].values.flatten()
    longitudes = data["lon"].values.flatten()
    print("Variables extracted: Temperature, Salinity, Latitude, Longitude.")
except KeyError as e:
    raise KeyError(f"Required variable missing: {e}")
except IndexError as e:
    raise IndexError(f"Issue extracting data: {e}")

# Convert to GeoJSON format
features = []
for i in range(len(latitudes)):
    try:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(longitudes[i]), float(latitudes[i])]
            },
            "properties": {
                "Temperature": float(temperature[i]) if i < len(temperature) else None,
                "Salinity": float(salinity[i]) if i < len(salinity) else None,
            }
        }
        features.append(feature)
    except IndexError as e:
        print(f"Index error while creating feature for point {i}: {e}")

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Save to GeoJSON file
geojson_file_path = "./puget_sound_data/puget_sound_data.geojson"
with open(geojson_file_path, "w") as f:
    json.dump(geojson_data, f, indent=2)
    print(f"GeoJSON file saved: {geojson_file_path}")
