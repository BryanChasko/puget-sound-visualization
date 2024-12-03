import xarray as xr

# Load the dataset
data = xr.open_dataset("./puget_sound_data/wod_osd_2021.nc")

# Inspect the dataset to check variable names and coordinates
print("Coordinates:", data.coords)
print("Variables:", data.variables)

# Explicitly set lat and lon as coordinates and create an index
data = data.set_index(lat='lat', lon='lon')

# Filter data for Puget Sound region (47.5° N to 48.5° N, 122.5° W to 123.5° W)
# Use lat and lon coordinates for filtering
puget_sound_data = data.sel(lat=slice(47.5, 48.5), lon=slice(-123.5, -122.5))

# Access specific variables of interest (e.g., temperature, salinity)
temperature = puget_sound_data["Temperature_obs"]
salinity = puget_sound_data["Salinity_obs"]

# Optionally save or analyze further
puget_sound_data.to_netcdf("puget_sound_filtered.nc")

# Optionally, print the filtered data to verify
print(puget_sound_data)
