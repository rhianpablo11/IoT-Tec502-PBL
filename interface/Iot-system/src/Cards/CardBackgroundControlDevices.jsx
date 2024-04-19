import styles from "./CardStyle.module.css"
import propsTypes from 'prop-types'

function CardBackgroundControlDevices(props){
    return(
        <div className={styles.cardControlBackground}>
            <h1>{props.nameDevice}</h1>
        </div>
    );
}

export default CardBackgroundControlDevices

CardBackgroundControlDevices.propsTypes ={
    nameDevice: propsTypes.string
}

CardBackgroundControlDevices.defaultProps ={
    nameDevice: 'Sensor da Sala'
}