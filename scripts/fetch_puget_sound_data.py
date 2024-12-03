import xarray as xr

# Load dataset and print key information
data = xr.open_dataset("./puget_sound_data/wod_osd_2021.nc")
print("Dataset loaded. Summary:")
print(data)

# Extract debugging information for later use
dataset_summary = {
    "coordinates": list(data.coords.keys()),
    "variables": list(data.variables.keys()),
    "dimensions": dict(data.dims),
    "attributes": dict(data.attrs)
}

def debug_info():
    """Prints debugging information about the dataset."""
    print("\n=== Dataset Debug Info ===")
    print("Coordinates:", dataset_summary["coordinates"])
    print("Variables:", dataset_summary["variables"])
    print("Dimensions:", dataset_summary["dimensions"])
    print("Attributes:", dataset_summary["attributes"])

# Ensure 'lat' and 'lon' are coordinates
if 'lat' in data.variables and 'lon' in data.variables:
    data = data.set_coords(["lat", "lon"])
else:
    try:
        data = data.assign_coords(lat=data['lat'], lon=data['lon'])
    except KeyError as key_error:
        debug_info()
        raise ValueError("Failed to set 'lat' and 'lon' as coordinates.") from key_error

# Verify dataset's coordinate range
print("Verifying dataset's coordinate ranges:")
print("Latitude range in dataset:", data["lat"].min().values, "to", data["lat"].max().values)
print("Longitude range in dataset:", data["lon"].min().values, "to", data["lon"].max().values)

# Adjusted boundaries for Puget Sound region (47.0°N to 48.5°N, 123.5°W to 122.0°W)
try:
    puget_sound_data = data.where(
        (data["lat"] >= 47.0) & (data["lat"] <= 48.5) &
        (data["lon"] >= -123.5) & (data["lon"] <= -122.0), drop=True
    )
    print("Filtering successful. Filtered data dimensions:", puget_sound_data.dims)
except ValueError as filter_error:
    debug_info()
    raise ValueError("Error during filtering.") from filter_error

# Extract variables of interest
try:
    temperature = puget_sound_data["Temperature"]
    salinity = puget_sound_data["Salinity"]
    print("Variables extracted: Temperature and Salinity.")
except KeyError as variable_error:
    debug_info()
    raise KeyError(f"Required variables not found: {variable_error}")

# Save filtered data with explicit encoding
filtered_file_path = "./puget_sound_data/puget_sound_filtered.nc"
try:
    encoding = {var: {"zlib": True, "complevel": 5} for var in puget_sound_data.variables}
    puget_sound_data.to_netcdf(filtered_file_path, encoding=encoding)
    print(f"Filtered dataset saved to: {filtered_file_path}")
except IOError as save_error:
    debug_info()
    raise IOError(f"Failed to save filtered dataset to {filtered_file_path}.") from save_error
