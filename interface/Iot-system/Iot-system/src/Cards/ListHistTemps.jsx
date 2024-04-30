import styles from "./CardStyle.module.css"

function ListHistTemps(props){
    return(
        <>
            <div className={styles.tempCardList}>
                <h1>Temp: {props.tempData[0]}ºC</h1>
                <h2>Date: {props.tempData[1]}</h2>
            </div>
        </>
    );
}

export default ListHistTemps