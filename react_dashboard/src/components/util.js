import _ from 'lodash';

export const parseInteger = (data) =>{
    const dataColumns = ['Rejected','drywaste_af','drywaste_bf','num_houses_doing_segg','num_houses_giving_mixwaste','num_houses_reached','wetwaste_af','wetwaste_bf'];
    dataColumns.map(col =>{
        _.each(data, item => item[col] = parseInt(item[col], 10));

    })
    return data;
}
export const getDropdownLanes = (data) =>{
    const lanes = _.map(data,'lane_name')
    const uniqueLanes = [...new Set(lanes)];
    return uniqueLanes;
}

export const calcTotalWaste = (data,selLane,cases) =>{
    let totWaste,caseCol;
    if(selLane ==='all'){
        caseCol = _.map(data,cases)
       
    }else{
        let selLaneData= data.filter(d => d.lane_name === selLane)
        caseCol = _.map(selLaneData,cases)
    }
    totWaste =  _.sum(caseCol);
    return totWaste;
}

export const calMonthlyData = (data,selLane,selCategory) =>{
    const month = {9:'Sep',10:'Oct',11:'Nov'}; 
    const colName = {'dry':'drywaste_af','wet':'wetwaste_af','rejected':'Rejected'};
    let selLaneData;
    if(selLane === 'all')
        selLaneData = data;
    else 
        selLaneData = data.filter(d => d.lane_name === selLane)
    const groupedData = selLaneData.reduce((obj,elem)=>{
        let category = parseInt(elem.date.split('/')[1]);
        if(!obj.hasOwnProperty(category))
            obj[category] = 0;
        
        obj[category] += elem[colName[selCategory]];
        return obj;
    },[])

    let calcLabels = [];
    let calcData = [];
    // console.log(groupedData);
    for(let key in groupedData){
        // console.log(month2[key]);
        calcLabels.push(month[key]);
        calcData.push(groupedData[key]);
    }
    for(let key in month){
      console.log(key);
  }
    // console.log(groupedData,calcData,calcLabels);
    const barData = {
        chartData:{
          labels: calcLabels,
          datasets:[
            {
              label:`${selCategory} waste`,
              data:calcData,
              backgroundColor:[
                'rgba(144, 238, 144, 0.6)',
                'rgba(144, 238, 144, 0.6)',
                'rgba(144, 238, 144, 0.6)',
              ]
            }
          ]
        }
      };
    return barData;
}


const createLabel = (oldArr,maxVal) =>{
    let arr = []
    let delta = Math.floor( oldArr.length / maxVal );

    for (let i = 0; i < oldArr.length; i=i+delta) {
        arr.push(oldArr[i]);
      }
      return arr;
}

export const calcDailyData = (selLanedata,selCategory) =>{
    const colName = {'dry':'drywaste_af','wet':'wetwaste_af','rejected':'Rejected'};
    const catData = _.map(selLanedata,colName[selCategory])
    const date = _.map(selLanedata,'date')
    const MAXVAL = 15;
    const xAxisLabel = createLabel(date,MAXVAL)
    
    const lineData = {
        chartData:{
          labels: xAxisLabel,
          datasets:[
            {
              label:`${selCategory} waste`,
              data:catData,
              fill: false,
              backgroundColor:'lightgreen',
              borderColor:'lightgreen',
              pointBackgroundColor:'grey'
            }
          ]
        }
      };
    return lineData;
}

export const sliceLaneData = (data,selLane) =>{
    if(selLane === 'all')
        return data;
    else
        return data.filter(d => d.lane_name === selLane);
}


export const groupDataByCategory = (data,selCategory) =>{
    const colName = {'dry':'drywaste_af','wet':'wetwaste_af','rejected':'Rejected'};
    const dataByCategory = data.reduce((obj,elem)=>{
      let category = elem["lane_name"];
      if(!obj.hasOwnProperty(category))
          obj[category] = 0;
      obj[category] += elem[colName[selCategory]]
      return obj;
  },[])

  return dataByCategory;
}


export const mergeGeomData = (geojson,dataByCategory) =>{
  const features = geojson.features;
  for(let key in features){
    let laneName = features[key].properties.name;
    features[key].properties['dataValue'] = dataByCategory[laneName];
  }

  return geojson;
  
}

