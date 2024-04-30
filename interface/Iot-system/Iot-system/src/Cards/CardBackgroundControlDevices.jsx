import { useEffect, useState } from "react";
import CardControlDevices from "./CardControlDevices";
import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'

function CardBackgroundControlDevices(props){
    const [device, setDevice] = useState('')
    useEffect(()=>{
        setDevice(props.device)
        console.log(device)
    },)
    if(device){
        return(
            <>
                <div className={styles.cardControlBackground}>
                    <h1>{device.name}</h1>
                    <h2>Ip address: {device.address}</h2>
                    <CardControlDevices device={props.device}/>
                </div>
            </>
        );
    }else{
        return(
            <>
                <div className={styles.cardControlBackground}>
                    <h1>{device.name}</h1>
                    <h2>{device.address}</h2>
                    <CardControlDevices device={props.device}/>
                </div>
            </>
        );
    }
    
}

export default CardBackgroundControlDevices

CardBackgroundControlDevices.propsTypes ={
    device: propsTypes.object
}

CardBackgroundControlDevices.defaultProps ={
    name: ' '
}