import React, {createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from 'axios';
import { API_URL } from "../constants";

// API Context 정의
interface AiPocContextType {
    postData: (url: string, data: any) => Promise<any>;
    loading: boolean;
    error: string | null;
}

const AiPocContext = createContext<AiPocContextType | undefined>(undefined);


export const AiPocProvider:React.FC<{ children: ReactNode}> = ({children}) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {

        // Cleanup
        return () => {
        };
    }, []);


    const postData = async (url: string, data: any) => {
        setLoading(true);
        setError(null);
        // Actions here

        setLoading(false)

    }


    return (
        <AiPocContext.Provider value={{postData, loading, error}}>
            {children}
        </AiPocContext.Provider>
    );

};

// // Hook을 사용하여 Context를 소비
// export const useApi = (): ApiContextType => {
//     const context = useContext(ApiContext);
//     if (context === undefined) {
//         throw new Error("useApi must be used within an ApiProvider");
//     }
//     return context;
// };



