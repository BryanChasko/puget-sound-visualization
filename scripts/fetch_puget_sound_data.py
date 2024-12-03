import xarray as xr

# Load the dataset
data = xr.open_dataset("./puget_sound_data/wod_osd_2021.nc")

# Inspect the dataset structure
print("Coordinates:", data.coords)
print("Variables:", data.variables)

# Ensure 'lat' and 'lon' are treated as coordinates and dimensions
if 'casts' in data.dims and 'lat' in data and 'lon' in data:
    print("Lat and Lon are not dimension coordinates. Converting...")
    data = data.set_index(index="casts").set_coords(["lat", "lon"])

# Filter data for the Puget Sound region (47.5° N to 48.5° N, 122.5° W to 123.5° W)
try:
    puget_sound_data = data.where(
        (data["lat"] >= 47.5) & (data["lat"] <= 48.5) &
        (data["lon"] >= -123.5) & (data["lon"] <= -122.5), drop=True
    )
except Exception as e:
    print("Error during filtering:", e)
    print("Latitude and longitude might not be structured as expected.")
    raise

# Check the filtered data
print("Filtered data:", puget_sound_data)

# Extract temperature and salinity variables
try:
    temperature = puget_sound_data["Temperature"]
    salinity = puget_sound_data["Salinity"]
except KeyError as e:
    print("Error accessing variables:", e)
    print("Available variables:", puget_sound_data.variables)
    raise

# Save the filtered dataset to a new NetCDF file
filtered_file_path = "./puget_sound_data/puget_sound_filtered.nc"
puget_sound_data.to_netcdf(filtered_file_path)
print(f"Filtered dataset saved to: {filtered_file_path}")
