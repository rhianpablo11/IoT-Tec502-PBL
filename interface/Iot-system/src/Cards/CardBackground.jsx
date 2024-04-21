import styles from "./CardStyle.module.css"
import logo from '../assets/logo.svg'
import propsTypes from 'prop-types'
import CardNoDevices from "./CardNoDevices";
import CardNewDeviceDetected from "./CardNewDeviceDetected";
import CardDevicesBackground from "./CardDevicesBackground";
import CardBackgroundControlDevices from "./CardBackgroundControlDevices";

function CardBackground(props){
    const data = new Date();
    data.getDate();
    const dataFormated =data.getHours()+':'+data.getMinutes()+' '+data.getDate()+'/'+(data.getMonth()+1)+'/'+data.getFullYear()
    let infoServer = 'desconnected'
    if(props.connection){
        infoServer = 'connected'
    }
    else{
        infoServer = 'desconnected'
    }

    let booleanoSubstituirPorContainIntensNaLista = false;
    if(booleanoSubstituirPorContainIntensNaLista){
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
                                {dataFormated}
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
                                {dataFormated}
                            </h3>
                            <br></br>
                            <h3>
                                server status: {infoServer}
                            </h3>
                        </div>
                    </div>
                    <div className={styles.mainScreen}>
                        <CardNewDeviceDetected type='temp sesor' address='52172'/>
                        <CardBackgroundControlDevices address='52172'/>
                        
                    </div>
                </div>
            </>
        );
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