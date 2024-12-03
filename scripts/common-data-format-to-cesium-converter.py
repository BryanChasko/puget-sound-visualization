import xarray as xr
import json

# Load the filtered dataset
data = xr.open_dataset("./puget_sound_data/puget_sound_ctd_filtered.nc")

# Extract relevant variables
lat = data["lat"].values
lon = data["lon"].values
temperature = data["Temperature"].isel(z_obs=0).values  # Surface-level data
salinity = data["Salinity"].isel(z_obs=0).values

# Combine data into GeoJSON format
geojson_features = []
for i in range(len(lat)):
    if not (temperature[i] or salinity[i]):  # Skip if no data
        continue
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(lon[i]), float(lat[i])],
        },
        "properties": {
            "Temperature": float(temperature[i]) if temperature[i] else None,
            "Salinity": float(salinity[i]) if salinity[i] else None,
        },
    }
    geojson_features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": geojson_features,
}

# Save to a GeoJSON file
output_path = "./puget_sound_data/puget_sound_ctd.geojson"
with open(output_path, "w") as f:
    json.dump(geojson_data, f, indent=2)

print(f"GeoJSON file saved to {output_path}")
