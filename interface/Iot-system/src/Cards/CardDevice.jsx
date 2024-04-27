import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'
import CardTempSensor from "./CardTempSensor";
import linesDesingTempSensor from '../assets/linhasCardDevice.svg'
import linesDesingSmartTV from '../assets/linhasCardDeviceTV.svg'
import React,{useEffect, useState, useContext} from "react";
import {DeviceSelectedContext} from './CardBackground'
import CardSmartTv from "./CardSmartTv";

function CardDevice(props){
    
    const [clicked, setClicked] = useState(false)
    const handleClick = (event) => {
        event.stopPropagation()
    }

    const getAssignAddress = (e) =>{
        if(clicked){
            props.assignAddress(props.device)
            setClicked(false)
        } else{
            props.assignAddress('')
            setClicked(true)
        }
        
    }
    if(props.device.type == 'temp sensor'){
        return(
            <div  onClick={handleClick} className={styles.backgroundDevice}>
                <button onClick={ getAssignAddress} >
                    <div className={styles.backgroundDeviceGradient}>
                        <div className={styles.backgroundDeviceLines}>
                            <img src={linesDesingTempSensor}></img>
                        </div>
                        <CardTempSensor device={props.device}/>
                    </div>
                    <h2>{props.device.name}</h2>
                </button>
                
            </div>
        );
    } else if(props.device.type == 'smart Tv'){
        return(
            <div  onClick={handleClick} className={styles.backgroundDevice}>
                <button onClick={ getAssignAddress} >
                    <div className={styles.backgroundDeviceGradient}>
                        <div className={styles.backgroundDeviceLines}>
                            <img src={linesDesingSmartTV}></img>
                        </div>
                        <CardSmartTv device={props.device} />
                    </div>
                    <h2>{props.device.name}</h2>
                </button>
                
            </div>
        )
    }
}

export default CardDevice

CardDevice.propsTypes ={
    nameDevice: propsTypes.string
}

CardDevice.defaultProps ={
    nameDevice: 'Sensor da Sala'
}