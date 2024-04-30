import styles from "./CardStyle.module.css"
import React,{useEffect, useState} from "react";

function CardNoDevices(){
    
    
    
    return(
        <div className={styles.subCardNoDevices}>
            <div  className={styles.textCenter}>
                <h1>
                    No devices connected!
                    <br></br>
                    Please wait for a device to be detected!
                </h1>
                
                
            </div>
        </div>
    );
}

export default CardNoDevices