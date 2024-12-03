import xarray as xr

# Load the filtered data
filtered_data = xr.open_dataset("./puget_sound_data/puget_sound_ctd_filtered.nc")

# Check the variables
print(filtered_data)
