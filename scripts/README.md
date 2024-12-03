# Puget Sound Visualization using NOAA WOD Data and Cesium

This repository demonstrates the process of accessing, filtering, and visualizing oceanographic data for the Puget Sound region using NOAA's **World Ocean Database (WOD)** to visualize in Cesium. It provides a step-by-step guide to set up AWS resources, download datasets, process data into a Cesium-compatible format, and render the visualization.

---

## **1. Objectives**

- Access NOAA WOD data for Puget Sound.
- Filter and extract relevant data for visualization.
- Convert data into a format compatible with Cesium (GeoJSON).
- Visualize oceanographic properties such as temperature and salinity on a 3D globe.

---

## **2. Workflow**

### **2.1 AWS Setup**

- **IAM User**: Create an IAM user with minimal permissions required for S3 and EC2 operations.
- **S3 Bucket**: Use an S3 bucket to store curated data for reuse.
- **EC2 Instance**: Set up an Amazon Linux 2023 instance to process the data efficiently.

### **2.2 Data Access**

1. **Explore Available Datasets**:
   Use the NOAA WOD S3 bucket to locate datasets:
   ```bash
   aws s3 ls s3://noaa-wod-pds/2021/ --recursive --no-sign-request
   ```
2. **Download Data**:
   Select and download relevant datasets:
   ```bash
   aws s3 cp s3://noaa-wod-pds/2021/wod_ctd_2021.nc ./puget_sound_data/ --no-sign-request
   ```

---

### **2.3 Data Processing**

1. **Filter Data**:
   Use Python and `xarray` to filter data for the geographic bounds of Puget Sound:
   ```python
   import xarray as xr

   # Load the dataset
   data = xr.open_dataset('./puget_sound_data/wod_ctd_2021.nc')

   # Filter for Puget Sound coordinates
   puget_sound_data = data.sel(lat=slice(47.5, 48.5), lon=slice(-123.5, -122.0))
   puget_sound_data.to_netcdf("./puget_sound_data/puget_sound_filtered.nc")
   ```

2. **Convert to GeoJSON**:
   Convert the filtered dataset into GeoJSON for Cesium visualization:
   ```python
   import geojson
   from geojson import Point, Feature, FeatureCollection

   # Iterate through dataset and create GeoJSON features
   features = []
   for i in range(len(puget_sound_data['lat'])):
       point = Point((puget_sound_data['lon'][i], puget_sound_data['lat'][i]))
       features.append(Feature(geometry=point, properties={
           "Temperature": float(puget_sound_data['Temperature'][i]),
           "Salinity": float(puget_sound_data['Salinity'][i])
       }))

   feature_collection = FeatureCollection(features)

   # Save to file
   with open('./puget_sound_data/puget_sound_data.geojson', 'w') as f:
       geojson.dump(feature_collection, f)
   ```

---

### **2.4 Visualization with Cesium**

1. **Load GeoJSON in Cesium**:
   Add the GeoJSON data to your Cesium app using `GeoJsonDataSource`:
   ```javascript
   var viewer = new Cesium.Viewer('cesiumContainer');

   Cesium.GeoJsonDataSource.load('./puget_sound_data.geojson').then(function (dataSource) {
       viewer.dataSources.add(dataSource);
       viewer.flyTo(dataSource);
   });
   ```

2. **Customize Visualization**:
   Apply styling based on properties (e.g., temperature, salinity).

---

## **3. Key Learnings**

- **Dataset Structure**: NOAA WOD data is complex but manageable using `xarray`.
- **Filtering Challenges**: Accurate coordinate filtering ensures only relevant data is visualized.
- **GeoJSON Conversion**: A straightforward format supported by Cesium for 3D mapping.

---

## **4. Dependencies**

- Python: `xarray`, `geojson`
- Cesium: A modern web browser and basic HTML/JavaScript knowledge.

---

## **5. Future Work**

- Extend analysis to include additional variables like chlorophyll and oxygen levels.
- Optimize visualization with clustering for large datasets.
- Explore integrating real-time data streams.

---

### **License**

This project uses open data provided by NOAA under their [Open Data License](https://www.noaa.gov/open-data).

--- 

This README is now suitable for public use and aligns with the original goals while preserving confidentiality. Let me know if there’s anything else to tweak!