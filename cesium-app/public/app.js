// Set the Cesium ion access token
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0YzNlNDliZS03YTQ0LTQ5YzMtODIxNy1iOTg1Mzc4YzAxMWEiLCJpZCI6MjU5ODQ5LCJpYXQiOjE3MzMyNzA3NjF9.sn6gmPhWs5Kn2Jjx5oMnJ7F1LX6_JITSEboREZEvWNE';

console.log('Cesium version:', Cesium.VERSION);

// Initialize the Cesium Viewer
const viewer = new Cesium.Viewer('cesiumContainer');

// Commented out the GeoJSON loading for now
// Load the GeoJSON file for Puget Sound visualization
 Cesium.GeoJsonDataSource.load('./puget_sound_data/puget_sound_data.geojson').then(function (dataSource) {
     viewer.dataSources.add(dataSource);
     viewer.flyTo(dataSource);
 });