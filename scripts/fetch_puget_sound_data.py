import xarray as xr

# Load the dataset
data = xr.open_dataset("./puget_sound_data/wod_osd_2021.nc")

# Inspect the dataset structure to understand coordinates and variables
print("Coordinates:", data.coords)
print("Variables:", data.variables)

# Ensure 'lat' and 'lon' are treated as coordinates
if 'lat' not in data.coords or 'lon' not in data.coords:
    print("Setting 'lat' and 'lon' as coordinates...")
    data = data.assign_coords(lat=data['lat'], lon=data['lon'])

# Filter data for the Puget Sound region (47.5° N to 48.5° N, 122.5° W to 123.5° W)
try:
    puget_sound_data = data.sel(lat=slice(47.5, 48.5), lon=slice(-123.5, -122.5))
except ValueError as e:
    print("Error during filtering:", e)
    print("Verifying the dimensions of 'lat' and 'lon'...")
    print("Latitude dimensions:", data['lat'].dims)
    print("Longitude dimensions:", data['lon'].dims)
    raise

# Check the filtered data
print("Filtered data:", puget_sound_data)

# Extract temperature and salinity variables
try:
    temperature = puget_sound_data["Temperature_obs"]
    salinity = puget_sound_data["Salinity_obs"]
except KeyError as e:
    print("Error accessing variables:", e)
    print("Available variables:", puget_sound_data.variables)
    raise

# Save the filtered dataset to a new NetCDF file
filtered_file_path = "./puget_sound_data/puget_sound_filtered.nc"
puget_sound_data.to_netcdf(filtered_file_path)
print(f"Filtered dataset saved to: {filtered_file_path}")
