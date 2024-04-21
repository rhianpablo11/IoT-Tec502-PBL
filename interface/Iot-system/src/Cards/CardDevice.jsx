import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'
import CardTempSensor from "./CardTempSensor";
import linesDesing from '../assets/linhasCardDevice.svg'
import React,{useEffect, useState, useContext} from "react";
import {DeviceSelectedContext} from './CardBackground'

function CardDevice(props){
    const [deviceSelected, setDeviceSelected] = useState(useContext(DeviceSelectedContext))

    return(
        <div  className={styles.backgroundDevice}>
            <button>
                <div className={styles.backgroundDeviceGradient}>
                    <div className={styles.backgroundDeviceLines}>
                        <img src={linesDesing}></img>
                    </div>
                    <CardTempSensor temperature={props.temp}/>
                </div>
                <h2>{props.nameDevice}</h2>
            </button>
            
        </div>
    );
}

export default CardDevice

CardDevice.propsTypes ={
    nameDevice: propsTypes.string
}

CardDevice.defaultProps ={
    nameDevice: 'Sensor da Sala'
}