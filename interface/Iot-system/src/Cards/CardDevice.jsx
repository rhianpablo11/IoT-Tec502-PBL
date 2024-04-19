import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'
import CardTempSensor from "./CardTempSensor";
import linesDesing from '../assets/linhasCardDevice.svg'

function CardDevice(props){
    return(
        <div className={styles.backgroundDevice}>
            <button>
                <div className={styles.backgroundDeviceGradient}>
                    <div className={styles.backgroundDeviceLines}>
                        <img src={linesDesing}></img>
                    </div>
                    <CardTempSensor />
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