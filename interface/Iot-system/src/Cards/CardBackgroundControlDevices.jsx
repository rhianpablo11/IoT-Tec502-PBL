import CardControlDevices from "./CardControlDevices";
import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'

function CardBackgroundControlDevices(props){
    
    return(
        <>
        
            <div className={styles.cardControlBackground}>
                <h1>{props.device.name}</h1>
                <CardControlDevices device={props.device}/>
            </div>
            
        </>


    );
}

export default CardBackgroundControlDevices

CardBackgroundControlDevices.propsTypes ={
    nameDevice: propsTypes.string
}

CardBackgroundControlDevices.defaultProps ={
    nameDevice: 'Sensor da Sala'
}