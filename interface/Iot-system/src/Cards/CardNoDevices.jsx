import styles from "./CardStyle.module.css"

function CardNoDevices(){
    
    return(
        <div className={styles.subCardNoDevices}>
            <div  className={styles.textCenter}>
                <h1>
                    No devices connected
                </h1>
                <button>
                    Search
                </button>
            </div>
        </div>
    );
}

export default CardNoDevices