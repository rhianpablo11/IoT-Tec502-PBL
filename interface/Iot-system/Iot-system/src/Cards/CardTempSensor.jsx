import styles from "./CardStyle.module.css"
import tempLogo from '../assets/tempSensor.svg'
import propsTypes from 'prop-types'

function CardTempSensor(props){

    if(props.device.deviceState == 'ligado'){
        return(
            <>
            
                <div className={styles.logoInMainCard}>
                    <img src={tempLogo}></img>
                </div>
                <div className={styles.mainInfoTemp}>
                    <h2>Temp:</h2>
                    <h1>{props.device.lastData[0][0]}ºC</h1>
                </div>
                <div className={styles.secondaryText}>
                    <h3>Date of last info</h3>
                </div>
                <div className={styles.valuesSecondary}>
                    <h3>{props.device.lastData[0][1]}</h3>
                    
                </div>
    
            </>
        );
    } else if(props.device.deviceState == 'stand-by'){
        return(
            <>
                <div className={styles.logoInMainCard}>
                    <img src={tempLogo}></img>
                </div>
                <div className={styles.mainInfoTempStateStandBy}>
                    <h2>Device State: </h2>
                    <h1>{props.device.deviceState}</h1>
                </div>
                <div className={styles.valuesSecondary}> 
                    <h4>For power-on click here
                        <br></br>
                        after go to section right
                    </h4>
                    
                </div>
    
            </>
        );
    }
    
}

export default CardTempSensor

CardTempSensor.propsTypes = {
    temperature: propsTypes.string,
    tempMinValue: propsTypes.string,
    tempMaxValue: propsTypes.string
}

CardTempSensor.defaultProps = {
    temperature: '35ºC',
    tempMinValue: '10ºC',
    tempMaxValue: '45ºC'
}