import React,{useState} from 'react'
import InfoBox from './InfoBox/InfoBox';
import './InfoBoxes.css';
import {calcTotalWaste} from '../util';
import _ from 'lodash';

export default function InfoBoxes({data,population,selLane,selCategory,setSelCategory}) {
    let dry = calcTotalWaste(data,population,selLane,'drywaste_af');
    let wet = calcTotalWaste(data,population,selLane,'wetwaste_af');
    let rejected = calcTotalWaste(data,population,selLane,'rejected');
    let total = calcTotalWaste(data,population,selLane,'total');
    let dry_percent = _.round(_.multiply(_.divide(dry[0],total[0]),100),3);
    let wet_percent = _.round(_.multiply(_.divide(wet[0],total[0]),100),3);
    let rej_percent = _.round(_.multiply(_.divide(rejected[0],total[0]),100),3);
    let total_percent = _.round(_.multiply(_.divide(total[0],total[0]),100),3);

    let date_array = data[data.length - 1].date.split('-');
    let latest_date= `${date_array[2]}-${date_array[1]}-${date_array[0]}`;

    // const [total,setTotal] = useState();
    return (
        <div className="infoboxes">
        <InfoBox active={selCategory === 'dry' } onClick={() => setSelCategory("dry")} title={`Recyclable Dry Waste`} value={`${dry[0]} kg`} percap={`${dry[1]} kg per capita`} percent={`${dry_percent} %`} date={`till ${latest_date}`}/>
        <InfoBox active={selCategory === 'wet' } onClick={() => setSelCategory("wet")} title={`Compostable Wet Waste`} value={`${wet[0]} kg`} percap={`${wet[1]} kg per capita`} percent={`${wet_percent} %`} date={`till ${latest_date}`}/>
        <InfoBox active={selCategory === 'rejected' } onClick={() => setSelCategory("rejected")} title={`Segregated Rejected Waste`} value={`${rejected[0]} kg`} percap={`${rejected[1]} kg per capita`} percent={`${rej_percent} %`} date={`till ${latest_date}`}/>
        <InfoBox active={selCategory === 'total' } onClick={() => setSelCategory("total")} title={`Total Waste`} value={`${total[0]} kg`} percap={`${total[1]} kg per capita`} percent={`${total_percent} %`} date={`till ${latest_date}`}/>
        </div>
    )
}