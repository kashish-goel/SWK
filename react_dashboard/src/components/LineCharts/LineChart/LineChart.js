import React,{} from 'react'
import {Line} from 'react-chartjs-2';
import './LineChart.css';

function Linechart({data, selLane,category}) {
    // const [state,setState] = useState();


      let titleText = `${selLane} Daily ${category} Waste Distribution`;
      titleText = titleText.charAt(0).toUpperCase() + titleText.slice(1)
      const options={
          title:{
            display:true,
            text:titleText,
            fontSize:20,
            // fontWeight: 1,
            lineHeight: 1.5,
            fontColor: "rgba(0, 0, 0, 0.54)",
            fontStyle:'normal',
            padding:20
          },
          legend:{
            display:false
            // position:
          },
          scales:{
            yAxes:[
              {
                ticks:{
                  beginAtZero: true,
                  // stepSize:200
                },
                
                  scaleLabel: {
                    display: true,
                    labelString: 'total waste(Kg)'
                  },
  
                  gridLines: {
                    // display:false,
                    // drawOnChartArea: false
                }
                
              }
            ],
            xAxes:[{
              gridLines:{
                // display:false
                drawOnChartArea: false
              }
            }
            ]
          }
  
        }

    return (
        <div className="linechart">
        <Line
          data={data.chartData}
          options={options}
        />
        </div>
    )
}

export default Linechart
