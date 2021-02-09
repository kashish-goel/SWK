import React,{useState} from 'react'
import InfoBox from './InfoBox/InfoBox';
import './InfoBoxes.css';
import {calcTotalWaste} from '../util';

export default function InfoBoxes({data,selLane,selCategory,setSelCategory}) {
    let dry = calcTotalWaste(data,selLane,'drywaste_af');
    let wet = calcTotalWaste(data,selLane,'wetwaste_af');
    let rejected = calcTotalWaste(data,selLane,'rejected');

    // const [dry,setDry] = useState();
    return (
        <div className="infoboxes">
        <InfoBox active={selCategory === 'dry' } onClick={() => setSelCategory("dry")} title={"Recyclable Dry Waste"} value={`${dry} kg`} description=""/>
        <InfoBox active={selCategory === 'wet' } onClick={() => setSelCategory("wet")} title={"Compostable Wet Waste"} value={`${wet} kg`} description=""/>
        <InfoBox active={selCategory === 'rejected' } onClick={() => setSelCategory("rejected")} title={"Segregated Rejected Waste"} value={`${rejected} kg`} description=""/>
        </div>
    )
}