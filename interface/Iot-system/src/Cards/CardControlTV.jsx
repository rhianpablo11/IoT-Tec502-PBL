import styles from "./CardStyle.module.css"
import youtubeLogo from '../assets/youtubeLogo.svg'
import netflixLogo from '../assets/netflixLogo.svg'
import liveTvLogo from '../assets/liveTvLogo.svg'
import amazonPrimeLogo from '../assets/primeVideoLogo.svg'
import { useState } from "react"
function CardControlTV(props){
    const addressBase = 'http://192.168.0.115:8082'
    const [appSelect, setAppSelected] = useState(props.device.lastData.app)
    
    const handleClick = (event) => {
        event.stopPropagation()
    }

    const chooseApp = async(app, event)=>{
        event.stopPropagation()
        const response = await fetch(addressBase+'/devices/tv/control/app', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': '111',
                'address': props.device.address.toString(),
                'app':app
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
    }


    if(props.device.deviceState == 'stand-by'){
        return(
            <div className={styles.graficArea}>
                <h1>
                    Sensor in Stand-by
                </h1>
            </div>
        );
    } else if(props.device.deviceState == 'ligado'){
        return(
            <div onClick={handleClick} className={styles.controlSmartTVArea}>
                <div className={styles.appsArea}>
                    <div >
                        <button onClick={(event) => chooseApp('Live Tv', event)}>
                            <img src={liveTvLogo}></img>
                        </button>
                    </div>
                    <div >
                        <button onClick={(event) => chooseApp('Amazon Prime', event)}>
                            <img src={amazonPrimeLogo}></img>
                        </button>
                    </div>
                    <div>
                        <button onClick={(event) => chooseApp('Youtube', event)}>
                            <img src={youtubeLogo}></img>
                        </button>
                    </div>
                    <div >
                        <button onClick={(event) => chooseApp('Netflix', event)}>
                            <img src={netflixLogo}></img>
                        </button>
                    </div>
                    
                
                    
                    
                </div>
                <div className={styles.comandsSmartTv}>
                    <div>
                        <h1>Vol: {props.device.lastData.volume}</h1>
                    </div>
                </div>
            </div>
        );
    } 
}

export default CardControlTV