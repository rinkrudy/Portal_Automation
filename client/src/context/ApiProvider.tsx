import React, {createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from 'axios';
import { API_URL } from "../constants";

// API Context 정의
interface ApiContextType {
    postData: (url: string, data: any) => Promise<any>;
    loading: boolean;
    error: string | null;
}

const ApiContext = createContext<ApiContextType | undefined>(undefined);


export const ApiProvider:React.FC<{ children: ReactNode}> = ({children}) => {
    const [data, setData] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);



    useEffect(() => {
        const fetchData = async () => {
            try {
                const url = "http://localhost:8000/api/test"
                const response = await axios.get(url)
                console.log(response)
                setData(response.data);
            }
            catch(error) {
                console.error('Failed to fetch dafa from Django api ', error);
            }
        }
        fetchData();

        // Cleanup
        return () => {
            console.log(data)
        };
    }, []);


    const postData = async (url: string, data: any) => {
        setLoading(true);
        setError(null);
        console.log(url);
        try {
            const response = await axios.post(url, data, {
                headers: {
                    'Content-Type' : 'multiparts/form-data',
                }
            });
            setLoading(false);
            return response.data
        } catch (err) {
            setLoading(false)
            console.error(err)
            setError("Error occured during the request(post)");
            throw err;
        }

    }


    return (
        <ApiContext.Provider value={{postData, loading, error}}>
            {children}
        </ApiContext.Provider>
    );


};

// Hook을 사용하여 Context를 소비
export const useApi = (): ApiContextType => {
    const context = useContext(ApiContext);
    if (context === undefined) {
        throw new Error("useApi must be used within an ApiProvider");
    }
    return context;
};



