import React,{useRef} from 'react'
import { Map, TileLayer , GeoJSON} from "react-leaflet";
import Control from 'react-leaflet-control';

import "./ChoroplethMap.css";
import { groupDataByCategory, mergeGeomData , getDomain} from "./../util";
import { scaleSequential } from "d3-scale";
import { interpolateGreens} from "d3-scale-chromatic";
import {extent} from 'd3-array'

function ChoroplethMap({geojson,data,setSelLane,selCategory}) {
    const geoJsonRef = useRef();
    const dataByCategory = groupDataByCategory(data,selCategory);
    const geojsonWithData = mergeGeomData(geojson,dataByCategory);
    const domain = Object.values(dataByCategory);
    const [min,max] = extent(domain);

    let colorScale= scaleSequential().domain([min,max]).interpolator(interpolateGreens);
    const  getColor = (d,min,max,mid) => {
        return d > max ? '#800026' :
               d > mid  ? '#E31A1C' :
               d > min   ? '#FEB24C' :
                          '#FFEDA0';
    }
    const purpleOptions = { color: 'lightgreen' }


    const handleMapClick = (e) => {
        setSelLane(e.target.feature.properties.name);
    }
    const onEachLane = (lane,layer) =>{
        // geoJsonRef.current.leafletElement.resetStyle(layer);
        if(geoJsonRef.current){
            console.log(geoJsonRef.current)
        }

        layer.bindPopup(lane.properties.name);
        // if(lane.properties.name ==='Bhandar Vada & Amar Prem chowk'){
        //     layer.options.style.color = "red";
        // }
        // if(lane.properties.name ==='HiraSethChawl - Waras Lane'){
        //     layer.options.style.color = "yellow";
        // }
        if(lane.properties.name ==='Navneet Lane to Tare Galli'){
            // console.log(layer);
            // layer.setStyle({fillColor :'blue'}) 
        layer.options.style.color = "green";
    }

    layer.options.fillOpacity = .8;

    // layer.options.style.color = getColor(lane.properties.dataValue,min,max,(max-min)/2);
    // layer.options.style.color = colorScale(lane.properties.dataValue);
    // console.log(layer.options.style.color);
    layer.on({
        click: handleMapClick,
        });
    }


    return (
        <div className="map">
    
       
        <Map center={[19.0182, 72.8168]} zoom={17} scrollWheelZoom={false}>
            <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

        {/* <TileLayer
          attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
        /> */}
            <GeoJSON key='my-geojson' style={purpleOptions} data={geojsonWithData} onEachFeature={onEachLane}  />
            <Control position="topright" >
                <div className="info">
                    <h4 style={{color:'white'}}>Click on polygon to select lane</h4>
                </div>
            </Control>

        </Map>

        </div>
    )
}

export default ChoroplethMap
