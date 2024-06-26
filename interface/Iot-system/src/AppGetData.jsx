import {useEffect, useState, createContext } from "react"
import CardBackground from "./Cards/CardBackground"
export const devicesDataContext = createContext()
import { API_URL } from "./ipBroker/ipBroker"

function AppGetData(){
    const [devicesData, setDevicesData] = useState([])
    const [serverState, setServerState] = useState(false)
    const addressBase = API_URL
    useEffect(()=>{
        const requisitSearchDevices = async() => {
            try{
                const response = await fetch((addressBase+'/devices').toString(),{
                method:'GET',
                headers: {
                    'Content-Type': 'application/json', // Se o conteúdo for JSON
                    // Outros cabeçalhos, se necessário
                  },
                })
                
                
                setDevicesData(await response.json())
                setServerState(true)
            }catch(Error){
                setDevicesData([])
                setServerState(false)
            }
            console.log('MAIS UMA VEZ', devicesData)
            
            
        }
        
        requisitSearchDevices()

        const interval = setInterval(requisitSearchDevices, 1000)
        return () => clearInterval(interval)
    },[])

    



    return (
        <>
            <devicesDataContext.Provider value={devicesData}>
                <CardBackground statusServer={serverState}/>
            </devicesDataContext.Provider>
            
        </>
    );
}

export default AppGetData