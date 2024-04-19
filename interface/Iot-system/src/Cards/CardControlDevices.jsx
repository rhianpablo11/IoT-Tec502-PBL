import styles from "./CardStyle.module.css"
import line from '../assets/dividingLine.svg'
import CardGraficTemp from "./CardGraficTemp"
import propsTypes from 'prop-types'

function CardControlDevices(props){
    let stateToPutDevice='stand-by'
    if(props.state == 'ligado'){
        stateToPutDevice = 'stand-by'
    } else if(props.state == 'stand-by'){
        stateToPutDevice = 'ligado'
    }
    return (
        <>
            <CardGraficTemp />
            <div className={styles.controlSection}>
                <img src={line}></img>
                <div className={styles.inputCamp}>
                    <input placeholder="New name for device"></input>
                    <button>Update</button>
                </div>
                <div className={styles.controlsSecondary}>
                    <h1>Controls:</h1>
                    <button>{stateToPutDevice}</button>
                    <button>Restart</button>
                    <button>Delete</button>
                </div>
            </div>
        </>
    );
}

CardControlDevices.propsTypes ={
    state: propsTypes.string
}

CardControlDevices.defaultProps = {
    state: 'ligado'
}

export default CardControlDevices