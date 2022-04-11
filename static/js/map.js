var mymap = L.map('mapid').setView([54.072, 116.213], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'}).addTo(mymap);
var geojson;

function resetHighlight(e) {
    var layer = e.target;
    // layer.bringToBack();
    geojson.resetStyle(e.target);
    info.update();
}

function style(feature) {
    return {
        fillColor: feature.properties.deposit ? '#FFE800': "#cccccc",
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        // layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function zoomToFeature(e) {
    console.log(e);
    mymap.fitBounds(e.target.getBounds());
}

function detailArea(e) {
    window.location.href = '/area_detail/' + e.target.feature.properties.id +'/'
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature,
        dblclick: detailArea
    });
}

geojson = L.geoJson(districtsData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(mymap);

var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Район:</h4>' + (props ?
        '<b>' + props.localname + '</b>'
        : 'Наведите на район');
};

info.addTo(mymap);