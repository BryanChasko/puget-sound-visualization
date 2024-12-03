// Initialize the Cesium Viewer
const viewer = new Cesium.Viewer('cesiumContainer', {
    terrainProvider: Cesium.createWorldTerrain(),
});

// Load the GeoJSON file for Puget Sound visualization
Cesium.GeoJsonDataSource.load('./puget_sound_data/puget_sound_data.geojson').then(function (dataSource) {
    viewer.dataSources.add(dataSource);
    viewer.flyTo(dataSource);
});
