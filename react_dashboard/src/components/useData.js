import {useState,useEffect} from 'react'
import {csv,json} from 'd3-request';  // only for testing on dummy data
import { parseInteger } from './util';

export const FetchData = () => {
    const [data,setData] = useState(null);
    useEffect(()=>{
        const url = "https://gist.githubusercontent.com/AnimeshN/229fb500cc795975547231297b0e7773/raw/4f5e46b549c483fcdeb8cb5d520e6b1df346537d/3_month_dummy_swk_cleaned_v1.1.csv";
        csv(url,d=>{
            const formattedData = parseInteger(d);
            setData(formattedData);
        });
    },[])
    return data;
}

export const FetchGeom = () =>{
    const [geom,setGeom] = useState(null);
    useEffect(()=>{
        const url = "https://gist.githubusercontent.com/AnimeshN/29199ffdba88fd7b4345ec64b54af732/raw/d1821894029a3315adad5c9c2a6dca16fe375381/dummy_lane_polygon_v1.1.geojson";
        json(url,g=>{
            setGeom(g);
        });
    },[])
    return geom;
}

