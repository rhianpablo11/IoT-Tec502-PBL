import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'
import tempSensor from '../assets/tempSensor.svg'
import smartTV from '../assets/smartTV.svg'


function CardNewDeviceDetected(props){
    let image = tempSensor;
    if(props.type == 'Temperature Sensor'){
        image = tempSensor
    } else if (props.type == 'Smart TV'){
        image = smartTV
    }
    return(
        <div className={styles.newDeviceFound} >
            <div>
                <h1>New device found</h1>
                <div className={styles.iconNewDevice}>
                    <img src={image}></img>
                </div>
                <div className={styles.infoDevice}>
                    <div className={styles.inputData}>
                        <h2>Name:</h2>
                        <input placeholder="Please, insert a name!"></input>
                    </div>
                    <div className={styles.inputData}>
                        <h2 >Type: </h2>
                        <div className={styles.retanguloInfo}>
                            <h2>{props.type}</h2>
                        </div>
                    </div>
                    <div className={styles.inputData}>
                        <h2>Address: </h2>
                        <div className={styles.retanguloInfo}>
                            <h2>{props.address}</h2>
                        </div>
                    </div>
                </div>
                <div className={styles.buttonAddDevice}>
                    <button>
                        Add Device
                    </button>
                </div>
            </div>
        </div>
    );
}

CardNewDeviceDetected.propsTypes = {
    type: propsTypes.string,
    address: propsTypes.string
}

CardNewDeviceDetected.defaultProps = {
    type: "Temperature Sensor",
    address: '173.16.103.10'
}

export default CardNewDeviceDetected