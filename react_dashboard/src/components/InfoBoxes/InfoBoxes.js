import React,{useState} from 'react'
import InfoBox from './InfoBox/InfoBox';
import './InfoBoxes.css';
import {calcTotalWaste} from '../util';

export default function InfoBoxes({data,selLane,selCategory,setSelCategory}) {
    let dry = calcTotalWaste(data,selLane,'drywaste_af');
    let wet = calcTotalWaste(data,selLane,'wetwaste_af');
    let rejected = calcTotalWaste(data,selLane,'Rejected');

    // const [dry,setDry] = useState();
    return (
        <div className="infoboxes">
        <InfoBox active={selCategory === 'dry' } onClick={() => setSelCategory("dry")} title={"Dry Waste After Seggregation"} value={`${dry} kg`} description=""/>
        <InfoBox active={selCategory === 'wet' } onClick={() => setSelCategory("wet")} title={"Wet Waste After Seggregation"} value={`${wet} kg`} description=""/>
        <InfoBox active={selCategory === 'rejected' } onClick={() => setSelCategory("rejected")} title={"Total Rejected Waste"} value={`${rejected} kg`} description=""/>
        </div>
    )
}
