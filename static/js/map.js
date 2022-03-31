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
        fillColor: "#cccccc",
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

updateMunicipals.filter(item => item.coords).forEach((item) => {
    var cmarker = L.circleMarker([item.lat, item.lng], {radius: 5})
    cmarker.bindPopup(`${item.name}<br>${item.km}км`);
    citiesItems.push(cmarker);
    var parent;
    if (item.firstRoad !== item.id, item.firstRoad) {
        parent = updateMunicipals.find(i => i.id === item.firstRoad);
        roadsFirstLevel.push(L.polyline([[item.lat, item.lng], [parent.lat, parent.lng]], {color: '#23cc23'}));
    }
    if (item.secondRoad !== item.id && item.secondRoad) {
        parent = updateMunicipals.find(i => i.id === item.secondRoad);
        roadsSecondLevel.push(L.polyline([[item.lat, item.lng], [parent.lat, parent.lng]], {color: '#ffff00'}));
    }
});

var cities = L.layerGroup(citiesItems);
var firstLevel = L.layerGroup(roadsFirstLevel);
var secondLevel = L.layerGroup(roadsSecondLevel);
firstLevel.addTo(mymap);
secondLevel.addTo(mymap);
cities.addTo(mymap);
var overlayMaps = {
    "Населенные пункты": cities,
    "Маршрутизация 1 звена": firstLevel,
    "Маршрутизация 2 звена": secondLevel,
};
L.control.layers({}, overlayMaps).addTo(mymap);


var greenIcon = L.icon({
    iconUrl: '/media/images/building.png',

    iconSize: [40, 40], // size of the icon
    iconAnchor: [40, 20], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});
var akcd = L.marker([52.033635, 113.501049], {icon: greenIcon, title: "АКДЦ"}).addTo(mymap);
akcd.bindTooltip("АКДЦ").openTooltip();
// L.marker([51.1063541,114.5030942], {icon: greenIcon}).addTo(mymap);


var drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
var topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(document.getElementById('app-bar'));
// topAppBar.setScrollTarget(document.getElementById('main-content'));
topAppBar.listen('MDCTopAppBar:nav', () => {
    drawer.open = !drawer.open;
});

document.querySelector("#button_map").addEventListener('click', () => {
    document.querySelector('#tableid').style.display = "none";
    document.querySelector('#mapid').style.display = "block";
    mymap.invalidateSize();
})

document.querySelector("#button_table").addEventListener('click', () => {
    document.querySelector('#tableid').style.display = "block";
    document.querySelector('#mapid').style.display = "none";
})
document.querySelectorAll('.mdc-select').forEach((item) => {
    new mdc.select.MDCSelect(item);
});