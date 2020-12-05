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
import { sliderLeft, sliderVertical } from 'd3-simple-slider';
import {FormControl,InputLabel,MenuItem, Select} from '@material-ui/core'







function ChoroplethMap({geojson,data,setSelLane,selCategory}) {
    const geoJsonRef = useRef();
    const dataByCategory = groupDataByCategory(data,selCategory);
    console.log(data)
    const geojsonWithData = mergeGeomData(geojson.zones,dataByCategory);
    const domain = Object.values(dataByCategory);
    const [min,max] = extent(domain);
    const [zoneControl,setZoneControl] = useState(false);
    let colorScale= scaleSequential().domain([min,max]).interpolator(interpolateRdYlGn);
    const svgLegRef = useRef();
    const svgSliderRef = useRef();




    // for(var i=0; i<parentDivs.length; i++)
    // {
    //     var children = parentDivs[i].getElementsByClassName("svg-color-legend");
    //     if(!children || children.length == 0)
    //     {
    //         parentDivs[i].style.display = "none";
    //     }
    // }


    // useEffect(() => {
        // const legend = select(svgSliderRef.current)
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


    // slider

    var sliderVertical = sliderLeft()
                            .min(1)
                            .max(30)
                            .step(1)
                            .height(300)
                            // .tickFormat(format('.2%'))
                            .ticks(5)
                            .default(0.015)
                            .on('onchange', val => {
                                console.log(val)
                            // d3.select('p#value-vertical').text(d3.format('.2%')(val));
                            });

    const slider = select(svgSliderRef.current)
                .attr('width', 100)
                .attr('height', 350)
                .append('g')
                .attr('transform', 'translate(60,30)');

    slider.call(sliderVertical);

   

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

    

    layer.options.fillOpacity = .8;

    
    layer.on({
        click: e => setSelLane(e.target.feature.properties.name),
        mouseover: e => {
           L.popup()
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
        <Control position="bottomright">
            <FormControl variant="outlined" >
                <InputLabel id="demo-simple-select-outlined-label">Age</InputLabel>
                    <Select
                        labelId="demo-simple-select-outlined-label"
                        id="demo-simple-select-outlined"
                        value={10}
                        // onChange={handleChange}
                        label="Age"
                        >
                        <MenuItem value="">
                            <em>None</em>
                        </MenuItem>
                        <MenuItem value={10}>Ten</MenuItem>
                        <MenuItem value={20}>Twenty</MenuItem>
                        <MenuItem value={30}>Thirty</MenuItem>
                    </Select>
        </FormControl>
        </Control>
        <Control position="bottomright">
        <svg id="svg-time-slider" ref={svgSliderRef}></svg>
        </Control>
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