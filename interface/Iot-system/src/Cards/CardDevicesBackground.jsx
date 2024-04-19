import CardDevice from "./CardDevice";
import styles from "./CardStyle.module.css"

function CardDevicesBackground(){
    return(
        <div className={styles.cardDeviceBackground}>
            <CardDevice />
            <CardDevice />
            <CardDevice />
            <CardDevice />
            
        </div>
    );
}

export default CardDevicesBackground