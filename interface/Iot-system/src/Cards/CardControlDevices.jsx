import styles from "./CardStyle.module.css"
import line from '../assets/dividingLine.svg'
import CardGraficTemp from "./CardGraficTemp"
import propsTypes from 'prop-types'
import { useEffect, useState } from "react"

function CardControlDevices(props){
    let stateToPutDevice='stand-by'
    let comandToggleStateForSend = '400'
    if(props.state == 'ligado'){
        stateToPutDevice = 'stand-by'
        comandToggleStateForSend = '106'        
    } else if(props.state == 'stand-by'){
        stateToPutDevice = 'ligado'
        comandToggleStateForSend = '105'
    }
    //console.log('OLAH EU AasQUI DINOVO ', props.address)
    const [deviceAddress, setDeviceAddress] = useState('')
    
    useEffect(()=>{
        setDeviceAddress(props.address)
    },)
    const sendUpdateNameDevice = async () =>{
        
        const newName = document.getElementById('UpdateNameDevice').value
        const response = await fetch('http://192.168.56.1:8082/devices', {
            method:'PUT',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'name': newName,
                'address': deviceAddress.toString()
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
        console.log(newName, props.address)
        document.getElementById('UpdateNameDevice').value = ''
    }
    
    const sendRestartDevice = async ()=>{
        
        const response = await fetch('http://192.168.56.1:8082/devices/control', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': '107',
                'address': deviceAddress.toString()
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
    }

    const sendToggleStateDevice = async()=>{
        
        const response = await fetch('http://192.168.56.1:8082/devices/control', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': comandToggleStateForSend,
                'address': deviceAddress.toString()
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
    }

    const sendDeleteDevice = async()=>{
        const response = await fetch('http://192.168.56.1:8082/devices/control', {
            method:'PATCH',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
              body: JSON.stringify({
                'comand': '108',
                'address': deviceAddress.toString()
              })
              
        })
        const resposta = await response.json
        console.log(resposta)
    }

    return (
        <>
            <CardGraficTemp />
            <div className={styles.controlSection}>
                <img src={line}></img>
                <div className={styles.inputCamp}>
                    <input id='UpdateNameDevice' placeholder="New name for device"></input>
                    <button onClick={sendUpdateNameDevice}>Update</button>
                </div>
                <div className={styles.controlsSecondary}>
                    <h1>Controls:</h1>
                    <button onClick={sendToggleStateDevice}>{stateToPutDevice}</button>
                    <button onClick={sendRestartDevice}>Restart</button>
                    <button onClick={sendDeleteDevice}>Delete</button>
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