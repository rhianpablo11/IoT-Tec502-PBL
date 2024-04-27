import styles from "./CardStyle.module.css"
import TvLogo from '../assets/smartTV.svg'


function CardSmartTv(props){
    if(props.device.deviceState == 'ligado'){
        return(
            <>
            
                <div className={styles.logoInMainCardTV}>
                    <img src={TvLogo}></img>
                </div>
                <div className={styles.mainInfoTV}>
                    <h2>Channel: </h2>
                    <h1>{props.device.lastData.channel} Ch</h1>    
                </div>
                <div className={styles.secondInfoTV}>
                    <h2>State: </h2>
                    <h1>{props.device.deviceState}</h1>
                </div>
                
                <div className={styles.secondaryTextTV}>
                    <h3>Vol:</h3>
                    <h2>{props.device.lastData.volume}</h2>
                </div>
                <div className={styles.valuesSecondaryTV}>
                    <h3>App on:</h3>
                    <h2>{props.device.lastData.app}</h2>
                </div>
    
            </>
        );
    } else if(props.device.deviceState == 'stand-by'){
        return(
            <>
                <div className={styles.logoInMainCardTV}>
                    <img src={TvLogo}></img>
                </div>
                <div className={styles.mainInfoTVStateStandBy}>
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

export default CardSmartTv