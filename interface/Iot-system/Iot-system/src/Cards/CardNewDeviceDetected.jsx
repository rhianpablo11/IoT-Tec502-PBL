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
    const changeName = async () =>{
        const name = document.getElementById('newNameDevice').value
        const response = await fetch('http://192.168.56.1:8082/devices', {
            method:'PUT',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
            body: JSON.stringify({
                'name': name,
                'address': props.address
            })
        })
        let resposta = await response.json
        console.log(resposta)
    }

    return(
        <div className={styles.putAlertInScreen}>
            <div className={styles.newDeviceFound} >
                <div>
                    <h1>New device found</h1>
                    <div className={styles.iconNewDevice}>
                        <img src={image}></img>
                    </div>
                    <div className={styles.infoDevice}>
                        <div className={styles.inputData}>
                            <h2>Name:</h2>
                            <input id='newNameDevice' placeholder="Please, insert a name!"></input>
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
                        <button onClick={changeName}>
                            Add Device
                        </button>
                    </div>
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