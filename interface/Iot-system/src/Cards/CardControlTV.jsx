import styles from "./CardStyle.module.css"
import youtubeLogo from '../assets/youtubeLogo.svg'
import netflixLogo from '../assets/netflixLogo.svg'
import liveTvLogo from '../assets/liveTvLogo.svg'
import amazonPrimeLogo from '../assets/primeVideoLogo.svg'
import { API_URL } from "../ipBroker/ipBroker"
import { useState } from "react"
function CardControlTV(props){
    const addressBase = API_URL
    const [appSelect, setAppSelected] = useState(props.device.lastData.app)
    const [volume, setVolume] = useState(0)
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

    const changeVolume = async(event)=>{
        setVolume(event.target.value)
        console.log('VOLUME: ', volume)
        const response = await fetch(addressBase+'/devices/tv/control/app', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': '110',
                'address': props.device.address.toString(),
                'app': event.target.value
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
    }

    const changeChannel = async(event)=>{
        console.log(event)
        console.log('VOLUME: ', event.target.outerText)
        let upOrDown = ''
        if(event.target.outerText == '-'){
            upOrDown = 'down'
        } else{
            upOrDown = 'up'
        }
        
        const response = await fetch(addressBase+'/devices/tv/control/app', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': '109',
                'address': props.device.address.toString(),
                'app': upOrDown
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
                    <div className={styles.appsButton}>
                        <button onClick={(event) => chooseApp('Live Tv', event)}>
                            <img src={liveTvLogo}></img>
                        </button>
                    </div>
                    <div className={styles.appsButton} >
                        <button onClick={(event) => chooseApp('Amazon Prime', event)}>
                            <img src={amazonPrimeLogo}></img>
                        </button>
                    </div>
                    <div className={styles.appsButton}>
                        <button onClick={(event) => chooseApp('Youtube', event)}>
                            <img src={youtubeLogo}></img>
                        </button>
                    </div>
                    <div className={styles.appsButton} >
                        <button onClick={(event) => chooseApp('Netflix', event)}>
                            <img src={netflixLogo}></img>
                        </button>
                    </div>
                    
                
                    
                    
                </div>
                <div className={styles.comandsSmartTv}>
                    <div className={styles.comandVolume}>
                        <h1>Vol: {volume}</h1>
                        <input className={styles.volume} onMouseUp={(event)=>changeVolume(event)}  type="range" min='0' max='100' />
                    </div>
                    <div className={styles.comandChannel}>
                        <h1>Channel:</h1>
                        <button onClick={(event) =>changeChannel(event)}><h1>-</h1></button>
                        <button onClick={(event) =>changeChannel(event)}><h1>+</h1></button>
                    </div>
                </div>
            </div>
        );
    } 
}

export default CardControlTV