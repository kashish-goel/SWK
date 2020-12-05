import React,{useRef,useState,useEffect} from 'react'
import { Map, TileLayer , GeoJSON, LayersControl,Marker,Popup,FeatureGroup,Circle} from "react-leaflet";
import Control from 'react-leaflet-control';

import "./ChoroplethMap.css";
import { groupDataByCategory, mergeGeomData , getDomain, getDropdownLanes} from "./../util";
import { scaleSequential } from "d3-scale";
import { interpolateRdYlGn,interpolateGreens,scaleQuantize} from "d3-scale-chromatic";
import {select} from "d3-selection";
import { legendColor } from 'd3-svg-legend'
import {format} from 'd3-format'
import {extent} from 'd3-array'
import 'd3-transition'
import L from 'leaflet';

function ChoroplethMap({geojson,data,setSelLane,selCategory}) {
    const geoJsonRef = useRef();
    const dataByCategory = groupDataByCategory(data,selCategory);
    const geojsonWithData = mergeGeomData(geojson.zones,dataByCategory);
    const domain = Object.values(dataByCategory);
    const [min,max] = extent(domain);
    const [zoneControl,setZoneControl] = useState(false);
    let colorScale= scaleSequential().domain([min,max]).interpolator(interpolateRdYlGn);
    const svgLegRef = useRef();


    // useEffect(() => {
        // const legend = select(svgLegRef.current)
        let legend = select("#svg-color-scale")
        legend.append("g")
        .attr("class", "svg-color-legend")
        .attr("transform", "translate(50,15)");


        let colorLegend = legendColor()
            .labelFormat(format(".2f"))
            .title(`Legend : ${selCategory} waste`)
            .scale(colorScale);

        

        legend.select(".svg-color-legend").call(colorLegend);
  

    
    // }, [dataByCategory])
    
    const zoneStyle = (e) =>{
        return {fillColor:colorScale(e.properties.dataValue)}
    }
    const spotsStyle = { color: 'red',fill:'black' }


    const onEachSpot = (spot,layer) =>{

    }
    const onEachLane = (lane,layer) =>{
        // geoJsonRef.current.leafletElement.resetStyle(layer);
        console.log(lane) 
        if(geoJsonRef.current){
            console.log(geoJsonRef.current)
        }

        // layer.bindPopup(`<b>${lane.properties.name}</b> <hr> <h1 class="text-center">${lane.properties.dataValue}</h1>`);
        // if(lane.properties.name ==='Bhandar Vada & Amar Prem chowk'){
        //     layer.options.style.color = "red";
        // }
        // if(lane.properties.name ==='HiraSethChawl - Waras Lane'){
        //     layer.options.style.color = "yellow";
        // }

    layer.options.fillOpacity = .8;

    // layer.options.style.color = getColor(lane.properties.dataValue,min,max,(max-min)/2);
    // layer.options.style.color = colorScale(lane.properties.dataValue);
    // console.log(layer.options.style.color);
    let popup;
    layer.on({
        click: e => setSelLane(e.target.feature.properties.name),
        mouseover: e => {
            popup = L.popup()
            .setLatLng(e.latlng)
            .setContent(`<b>${e.target.feature.properties.name}</b> <hr> <h1 class="text-center" style={color:lightgreen}>${e.target.feature.properties.dataValue} kg</h1> `)
            .openOn(layer._map);
        },
        mouseout: e=> layer._map.closePopup()
        });

    }

    const pointToLayer = (feature,latlong) =>{
        return L.circleMarker(latlong, {radius:5});
    }

    const showZoneControl = (e)=>{
        if(e.name === 'Zones')
            setZoneControl(true)
    }

    const removeZoneControl = (e) =>{
        if(e.name === 'Zones')
            setZoneControl(false)
    }

    let zoneControlDiv;
    if(true){
        zoneControlDiv =  <Control position="bottomleft" className="legend-div">
        <div className="info">
            <h4 style={{fontSize:"15px",fontWeight:"bold"}}>Click on polygon to select lane</h4>
        </div>
        <svg className = "svg-legend" ref={svgLegRef} id="svg-color-scale"></svg>

    </Control>
    }else{
        zoneControlDiv
    }
           
    let geojsonMap =  <GeoJSON key='my-geojson' style={zoneStyle} data={geojsonWithData} onEachFeature={onEachLane}  />
    return (
        <div className="map">
    
       
        <Map center={[19.0182, 72.8168]} zoom={17} scrollWheelZoom={false} onOverlayadd={ showZoneControl } onoverlayremove={ removeZoneControl }>
            <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
        {zoneControlDiv}
        {/* <TileLayer
          attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
          url='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
        /> */}
            {geojsonMap}
            
            <LayersControl position="topright">
                
                <LayersControl.BaseLayer name="Default">
                    <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                </LayersControl.BaseLayer>

                <LayersControl.BaseLayer name="Grey scale">
                    <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"
                    />
                </LayersControl.BaseLayer>


                <LayersControl.Overlay name="Spots">
                    <GeoJSON key='my-geojson' style={spotsStyle} data={geojson.spots} pointToLayer={pointToLayer} onEachFeature={onEachSpot}/>
                </LayersControl.Overlay>
                {/* <LayersControl.Overlay name="Zones"  >
                  

                    <FeatureGroup >
                       {geojsonMap}
                        
                    </FeatureGroup>
                </LayersControl.Overlay> */}
                </LayersControl>


        </Map>

        </div>
    )
}

export default ChoroplethMap