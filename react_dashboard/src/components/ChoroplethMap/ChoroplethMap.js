import React,{useRef,useState} from 'react'
import { Map, TileLayer , GeoJSON,LayersControl} from "react-leaflet";
import Control from 'react-leaflet-control';

import "./ChoroplethMap.css";
import { groupDataByCategory, mergeGeomData , groupDataByDateCategory} from "./../util";
import { scaleSequential } from "d3-scale";
import { interpolateRdYlGn} from "d3-scale-chromatic";
import {select} from "d3-selection";
import { legendColor } from 'd3-svg-legend'
import {format} from 'd3-format'

import {extent} from 'd3-array'
// import * as d3 from 'd3';

import 'd3-transition'
import L from 'leaflet';
// import { sliderLeft, sliderVertical } from 'd3-simple-slider';
import {FormControl,InputLabel,MenuItem, Select} from '@material-ui/core'
// import * as d3 from 'd3';
import { sliderLeft, sliderVertical } from 'd3-simple-slider';





function ChoroplethMap({geojson,data,setSelLane,selCategory}) {
    const geoJsonRef = useRef();
    const dataByCategory = groupDataByCategory(data,selCategory);
    const [zoneControl,setZoneControl] = useState(false);
    const svgLegRef = useRef();
    const svgSliderRef = useRef();
    const [selMonth, setSelMonth] = useState('10');
    const [selDay, setSelDay] = useState(1);

    const dataByDateCategory = groupDataByDateCategory(data,selCategory,selMonth,selDay)
    console.log(dataByDateCategory)
    const geojsonWithData = mergeGeomData(geojson,dataByDateCategory);
    console.log(geojsonWithData)

    const domain = []
    for( let key in dataByDateCategory){
        domain.push(dataByDateCategory[key])
    }
     console.log(domain)
    const [min,max] = extent(domain);

    let colorScale= scaleSequential().domain([min,max]).interpolator(interpolateRdYlGn);
  
    let legend = select("#svg-color-scale")
    legend.append("g")
    .attr("class", "svg-color-legend")
    .attr("transform", "translate(50,15)");
    console.log(selCategory)
    let newtitle;
    if(selCategory=='dry'){
      newtitle=`Recyclable Dry Waste`
    }
    else if(selCategory=='wet'){
      newtitle=`Compostable Wet Waste`
    }
    else if(selCategory=='rejected'){
        newtitle=`Seggregated Rejected Waste`
      }
    let colorLegend = legendColor()
        .labelFormat(format(".2f"))
        .title(`Legend : ${newtitle}(Kgs)`)
        .scale(colorScale);

    

    legend.select(".svg-color-legend").call(colorLegend);



// }, [dataByCategory])


// slider
var sliderVertical = sliderLeft()
    .min(1)
    .max(30)
    .step(1)
    .height(300)
    // .tickFormat(d3.format('.2%'))
    .ticks(5)
    .default(0.015)
    .on('onchange', val => {
        setSelDay(val)
    });

  var gVertical = select(svgSliderRef.current)
    // .append('svg')
    .attr('width', 100)
    .attr('height', 400)
    .append('g')
    .attr('transform', 'translate(60,30)');

  gVertical.call(sliderVertical);

//   d3.select('p#value-vertical').text(d3.format('.2%')(sliderVertical.value()));
// var sliderVertical = sliderLeft()
//                         .min(1)
//                         .max(30)
//                         .step(1)
//                         .height(300)
//                         // .tickFormat(format('.2%'))
//                         .ticks(5)
//                         .default(0.015)
//                         .on('onchange', val => {
//                             setSelDay(val)
//                         // d3.select('p#value-vertical').text(d3.format('.2%')(val));
//                         });

// const slider = select(svgSliderRef.current)
//             .attr('width', 100)
//             .attr('height', 350)
//             .append('g')
//             .attr('transform', 'translate(60,30)');

// slider.call(sliderVertical);



const zoneStyle = (e) =>{
    if(typeof e.properties.dataValue !== "undefined")
    return { fillColor:colorScale(e.properties.dataValue), color:"black" }
    else
    return { fillColor:"black",color:"black" }
}
const spotsStyle = { color: 'red',fill:'black',color:"black" }


const onEachSpot = (spot,layer) =>{

}
const onEachLane = (lane,layer) =>{
    // geoJsonRef.current.leafletElement.resetStyle(layer);
    // if(geoJsonRef.current){
    //     console.log(geoJsonRef.current)
    // }


const setDataValue = value =>{
    if(typeof value !== "undefined")
        return `<h1 class="text-center">${value} kg</h1>`
    else    
        return `<h5 class="text-center">Data not Found</h5>`
}
layer.options.fillOpacity = .8;


layer.on({
    click: e => {
        let zone_id = e.target.feature.properties.zone_id;
        console.log(zone_id)
        if(zone_id !== 'zone_4' && zone_id !=='zone_5' && zone_id !== 'zone_9' && zone_id !=='' )
            setSelLane(zone_id)
    },
    mouseover: e => {
       L.popup()
        .setLatLng(e.latlng)
        .setContent(`<b>${e.target.feature.properties.zone_name}</b> <hr> ${setDataValue(e.target.feature.properties.dataValue)}`)
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
        <h4 style={{fontSize:"15px",fontWeight:"bold",marginLeft:"100px"}}>Click on polygon to select lane</h4>
    </div>
    <svg className = "svg-legend" ref={svgLegRef} id="svg-color-scale" style={{fontSize:"13px",marginLeft:"50px"}}></svg>

</Control>
}else{
    zoneControlDiv
}
       
let geojsonMap =  <GeoJSON key='my-geojson' style={zoneStyle} data={geojsonWithData} onEachFeature={onEachLane}  />

const handleDropdownChange = (e) =>{
    setSelMonth(e.target.value)
}
return (
    <div className="map">

   {/* <div className="map__choropleth"> */}
    <Map center={[19.0202, 72.8168]} zoom={16.5} scrollWheelZoom={false} onOverlayadd={ showZoneControl } onoverlayremove={ removeZoneControl }>
        <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
    <Control position="topright">
        <FormControl variant="filled" >
            <InputLabel id="demo-simple-select-filled-label">Month</InputLabel>
                <Select
                    labelId="demo-simple-select-outlined-label"
                    id="demo-simple-select-outlined"
                    value={selMonth}
                    onChange={handleDropdownChange}
                    label="Month"
                    className="month-drop"
                    >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    <MenuItem value={'09'}>September</MenuItem>
                    <MenuItem value={'10'}>October</MenuItem>
                    <MenuItem value={'11'}>November</MenuItem>
                    <MenuItem value={'12'}>December</MenuItem>
                    <MenuItem value={'01'}>January</MenuItem>
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

    {/* </div> */}
    {/* <div className="map__slider"></div> */}

    </div>
)
}

export default ChoroplethMap