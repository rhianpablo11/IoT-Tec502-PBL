import { useEffect, useState } from "react";
import styles from "./CardStyle.module.css"
import Chart from 'react-apexcharts'
import ListHistTemps from "./ListHistTemps";

function CardGraficTemp(props){
    const [listTemps, setListTemps] = useState([['','']])
    
    useEffect(()=>{
        if(Array.isArray(props.device.lastData)){
            
            setListTemps(props.device.lastData.filter(
                item=>item[0]!='none'
            ))
            
        }
        
        
    },)
    if(props.device.deviceState == 'stand-by'){
        return(
            <div className={styles.graficArea}>
                <h1>
                    Sensor in Stand-by
                </h1>
            </div>
        );
    } else if(props.device.deviceState == 'ligado'){
        
        return(
            <>
                <div className={styles.graficArea}> 
                    <ul>
                        {listTemps.map((temp, index)=>
                            
                            <li >
                                <ListHistTemps  tempData={temp}/>
                            </li>)} 
                    </ul>
                        
                </div>
            </>
            
        );
    }
    
}

export default CardGraficTemp