import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'

function CardDevice(props){
    return(
        <div className={styles.backgroundDevice}>
            <button>
                <div className={styles.backgroundDeviceGradient}>

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