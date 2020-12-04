import React from 'react'
import { FormControl, MenuItem, Select } from '@material-ui/core';
import {getDropdownLanes} from '../util';
import './Dropdown.css';

 
export default function Dropdown({data, selLane,setSelLane}) {
    const lanes = getDropdownLanes(data);
    return (
        
        <FormControl className="dropdown">
          <Select id="lane-dropdown" variant="outlined" value={selLane} onChange={e=>{setSelLane(e.target.value)}}>
            <MenuItem key='all' value="all">All</MenuItem>
            {lanes.map(lane =>(
               <MenuItem key={lane}value={lane}>{lane}</MenuItem> 
            ))}
          </Select>
      </FormControl>
    )
}
