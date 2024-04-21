import {useEffect, useState, createContext } from "react"
import CardBackground from "./Cards/CardBackground"
export const devicesDataContext = createContext()

function AppGetData(){
    const [devicesData, setDevicesData] = useState([])
    useEffect(()=>{
        const requisitSearchDevices = async() => {
            const response = await fetch('http://192.168.56.1:8082/devices',{
                method:'GET',
                headers: {
                    'Content-Type': 'application/json', // Se o conteúdo for JSON
                    // Outros cabeçalhos, se necessário
                  },
            })
            
            setDevicesData(await response.json())
            
        }
        requisitSearchDevices()
        
        const interval = setInterval(requisitSearchDevices, 3000)
        return () => clearInterval(interval)
    }, [])
    return (
        <>
            <devicesDataContext.Provider value={devicesData}>
                <CardBackground />
            </devicesDataContext.Provider>
            
        </>
    );
}

export default AppGetData