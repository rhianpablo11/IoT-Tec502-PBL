import CardDevice from "./CardDevice";
import styles from "./CardStyle.module.css"
import React,{useEffect, useState, useContext} from "react";
import { devicesDataContext } from "../AppGetData";
import {DeviceSelectedContext} from './CardBackground'

function CardDevicesBackground(props){
    
    const [devicesList, setDevicesList] = useState([])
    const devices = useContext(devicesDataContext)
    //console.log(devices)
    useEffect(() =>{
        setDevicesList(devices)
    },)

    function setDeviceChoice(i){
        setDeviceSelected(devicesList[i])
        console.log(devicesList[i])
    }



    const [clicked, setClicked] = useState(false)
    const handleClick = () => {
        if (clicked === true) {
          setClicked(false)
        } else if (clicked === false) {
          setClicked(true)
        }
      }
    
    const [deviceSelected, setDeviceSelected] = useState('')
    const testeReceber = (address) => {
        console.log('SOU EU',address)
        setDeviceSelected(address)
        props.assignDeviceControl(address)
    }


    return(
        <div className={styles.cardDeviceBackground}>
            <ul>
                {devices.map((device, index)=>
                    
                    <li >
                        <CardDevice assignAddress={testeReceber} devic={device} nameDevice={device.name} temp={device.lastData[0][0]} address={device.address}/>
                    </li>)} 
            </ul>
        </div>
    );
}

export default CardDevicesBackground