import CardDevice from "./CardDevice";
import styles from "./CardStyle.module.css"
import React,{useEffect, useState} from "react";

function CardDevicesBackground(){

    const [devicesList, setDevicesList] = useState([])
    useEffect(()=>{
        const requisitSearchDevices = async() => {
            const response = await fetch('http://192.168.56.1:8082/devices',{
                method:'GET',
                headers: {
                    'Content-Type': 'application/json', // Se o conteúdo for JSON
                    // Outros cabeçalhos, se necessário
                  },
            })
            
            setDevicesList(await response.json())
            console.log(devicesList)
        }
        requisitSearchDevices()
        
        const interval = setInterval(requisitSearchDevices, 2000)
        return () => clearInterval(interval)
    }, [])
    return(
        <div className={styles.cardDeviceBackground}>
            <ul>
                {devicesList.map((device, index)=>
                    
                    
                    <li>
                        <CardDevice nameDevice={device.name} temp={device.lastData[0][0]}/>
                    </li>)} 
            </ul>
        </div>
    );
}

export default CardDevicesBackground