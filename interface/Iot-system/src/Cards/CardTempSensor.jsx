import styles from "./CardStyle.module.css"
import tempLogo from '../assets/tempSensor.svg'
import propsTypes from 'prop-types'

function CardTempSensor(props){

    return(
        <>
        
            <div className={styles.logoInMainCard}>
                <img src={tempLogo}></img>
            </div>
            <div className={styles.mainInfoTemp}>
                <h2>Temp:</h2>
                <h1>{props.temperature}ºC</h1>
            </div>
            <div className={styles.secondaryText}>
                <h3 className={styles.tempMin}>Temp min: </h3>
                <h3 className={styles.tempMax}>Temp max: </h3>
            </div>
            <div className={styles.valuesSecondary}>
                <h3>{props.tempMinValue}</h3>
                <h3 className={styles.tempMax}>{props.tempMaxValue}</h3>
            </div>

        </>
    );
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