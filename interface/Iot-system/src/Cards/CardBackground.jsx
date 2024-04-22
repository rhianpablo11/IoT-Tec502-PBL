import styles from "./CardStyle.module.css"
import logo from '../assets/logo.svg'
import propsTypes from 'prop-types'
import CardNoDevices from "./CardNoDevices";
import CardNewDeviceDetected from "./CardNewDeviceDetected";
import CardDevicesBackground from "./CardDevicesBackground";
import CardBackgroundControlDevices from "./CardBackgroundControlDevices";
import CardControlDevices from "./CardControlDevices";
import { useState, useEffect, useContext, createContext } from "react";
import { devicesDataContext } from "../AppGetData.jsx";
export const DeviceSelectedContext = createContext()

function CardBackground(props){
    const [deviceSelected, setDeviceSelected] = useState('')
    const [dateClock, setDateClock] = useState(new Date())
    const [devicesList, setDevicesList] = useState([])
    const devices = useContext(devicesDataContext)
    const [devicesListIsEmpty, setDeviceListState] = useState(false);
    //console.log(devices)
    function setDeviceForControl(device){
        setDeviceSelected(device)
        console.log('DEMOREI MAIS CHEGUEI PIVETE ', device)
        return device
    }
    useEffect(()=>{
        setDevicesList(devices)
        console.log('esse car',devices)
        
        for(let i=0;i<devices.length;i++){
            if(devices[i].address == deviceSelected.address){
                setDeviceForControl(devices[i])
            }
        }

        if(devicesList.length>0){
            setDeviceListState(true)
        } else{
            setDeviceListState(false)
        }
    },)

    useEffect(()=>{
        
        const intervalDate = setInterval(()=>{
            setDateClock(new Date())
        }, 1000)
        return ()=>{
            clearInterval(intervalDate)
        }
    }, [])

    function formatDateClock(){
        const hours = dateClock.getHours()
        const minutes = dateClock.getMinutes()
        const seconds = dateClock.getSeconds()
        const day = dateClock.getDate()
        const month = dateClock.getMonth()+1
        const year = dateClock.getFullYear()
        return `${addZero(hours)}:${addZero(minutes)}:${addZero(seconds)} ${addZero(day)}/${addZero(month)}/${year}`
    }

    function addZero(num){
        if(num<10){
            return '0'+num
        } else{
            return num
        }
    }
    


    let infoServer = 'desconnected'
    if(props.statusServer){
        infoServer = 'connected'
        if(!devicesListIsEmpty){
            return(
                <>
                    <div className={styles.cardBackground}>
                        
                        <div className={styles.topElements}>
                            <div className={styles.greetingUser}>
                                <h2>
                                    Bom dia, {props.name} 
                                </h2>
                            </div>
                            <div className={styles.logo}>
                                <a href="#">
                                    <img src={logo}>
                                    </img>
                                </a>
                            </div>
                            <div className={styles.informations}>
                                <h3>
                                    {formatDateClock()}
                                </h3>
                                <br></br>
                                <h3>
                                    server status: {infoServer}
                                </h3>
                            </div>
                        </div>
                        <div className={styles.mainScreen}>
                            <CardNoDevices />
                        </div>
                    </div>
                </>
            );
        } else{
            return(
                <>
                    <div className={styles.cardBackground}>
                        
                        <div className={styles.topElements}>
                            <div className={styles.greetingUser}>
                                <h2>
                                    Bom dia, {props.name} 
                                </h2>
                            </div>
                            <div className={styles.logo}>
                                <a href="#">
                                    <img src={logo}>
                                    </img>
                                </a>
                            </div>
                            <div className={styles.informations}>
                                <h3>
                                    {formatDateClock()}
                                </h3>
                                <br></br>
                                <h3>
                                    server status: {infoServer}
                                </h3>
                            </div>
                        </div>
                        <div className={styles.mainScreen}>
                        
                                <CardDevicesBackground assignDeviceControl={setDeviceForControl}/>
                                <CardBackgroundControlDevices device={deviceSelected}/>
                        </div>
                    </div>
                </>
            );
        }
    }
    else{
        infoServer = 'desconnected'
        return(
            <>
                    <div className={styles.cardBackground}>
                        
                        <div className={styles.topElements}>
                            <div className={styles.greetingUser}>
                                <h2>
                                    Bom dia, {props.name} 
                                </h2>
                            </div>
                            <div className={styles.logo}>
                                <a href="#">
                                    <img src={logo}>
                                    </img>
                                </a>
                            </div>
                            <div className={styles.informations}>
                                <h3>
                                    {formatDateClock()}
                                </h3>
                                <br></br>
                                <h3>
                                    server status: {infoServer}
                                </h3>
                            </div>
                        </div>
                        <div className={styles.mainScreen}>
                            
                        </div>
                    </div>
                </>
        )
    }

    

    


    
    

    
}


CardBackground.propsTypes = {
    name: propsTypes.string,
    connected: propsTypes.bool
}

CardBackground.defaultProps ={
    name: "Rhian Pablo",
    connection: true
}
export default CardBackground