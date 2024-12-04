// Set the Cesium ion access token
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0YzNlNDliZS03YTQ0LTQ5YzMtODIxNy1iOTg1Mzc4YzAxMWEiLCJpZCI6MjU5ODQ5LCJpYXQiOjE3MzMyNzA3NjF9.sn6gmPhWs5Kn2Jjx5oMnJ7F1LX6_JITSEboREZEvWNE';

console.log('Cesium version:', Cesium.VERSION);

// Initialize the Cesium Viewer
const viewer = new Cesium.Viewer('cesiumContainer');

// Define the data points within Puget Sound
const dataPoints = [
    { lat: 47.6, lon: -122.3, temperature: 10.5, salinity: 30.1 },
    { lat: 47.7, lon: -122.4, temperature: 11.0, salinity: 29.8 },
    { lat: 47.8, lon: -122.5, temperature: 10.8, salinity: 30.0 },
    { lat: 47.9, lon: -122.6, temperature: 10.7, salinity: 30.2 },
    { lat: 48.0, lon: -122.7, temperature: 10.9, salinity: 29.9 }
];

// Add the data points to the Cesium Viewer
dataPoints.forEach(point => {
    viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(point.lon, point.lat),
        point: {
            pixelSize: 10,
            color: Cesium.Color.RED
        },
        label: {
            text: `Temp: ${point.temperature}°C\nSalinity: ${point.salinity}`,
            font: '14pt monospace',
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 2,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            pixelOffset: new Cesium.Cartesian2(0, -9)
        }
    });
});

// Fly to the data points
viewer.zoomTo(viewer.entities);