import React,{} from 'react'
import {Bar} from 'react-chartjs-2';
import './Barchart.css';
import { calMonthlyData } from '../util';

function Barchart({data,selLane,selCategory}) {
    // const [state,setState] = useState();
    const barData = calMonthlyData(data,selLane,selCategory);
    const upperCaseSelCategory = selCategory.charAt(0).toUpperCase() + selCategory.slice(1)
    const upperCaseSelLane = selLane.charAt(0).toUpperCase() + selLane.slice(1)

    let titleText = `${upperCaseSelLane} Monthly ${upperCaseSelCategory} Waste Distribution`;

    return (
        <div className="barchart">
        <Bar
          data={barData.chartData}
          options={{
            title:{
              display:true,
              text:titleText,
              fontSize:20,
              // fontWeight: 1,
              lineHeight: 1.5,
              fontColor: "rgba(0, 0, 0, 0.54)",
              fontStyle:'normal',
              // padding:10
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

          }}
        />
        </div>
    )
}

export default Barchart
