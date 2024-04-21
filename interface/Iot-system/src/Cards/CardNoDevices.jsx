import styles from "./CardStyle.module.css"
import React,{useState} from "react";

function CardNoDevices(){
    let devicesList = [];
    const requisitSearchDevices = async() => {
        const response = await fetch('http://192.168.56.1:8082/devices',{
            method:'GET',
            headers: {
                'Content-Type': 'application/json', // Se o conteúdo for JSON
                // Outros cabeçalhos, se necessário
              },
            
            
        })
        devicesList = await response.json()
        console.log(devicesList)
    }
    
    return(
        <div className={styles.subCardNoDevices}>
            <div  className={styles.textCenter}>
                <h1>
                    No devices connected
                </h1>
                <button onClick={requisitSearchDevices}>
                    Search  
                </button>
            </div>
        </div>
    );
}

export default CardNoDevices