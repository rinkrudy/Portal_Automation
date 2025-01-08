import { useEffect, useState } from 'react';

type ConfigType = {
    Mode: string;
    ModeList: string[];
};

const useConfig = (configUrl: string) => {
    const [config, setConfig] = useState<ConfigType | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchConfig = async () => {
            try {

                const response = await fetch(configUrl);

                if (response.ok === false) throw new Error("Failed to load config");
                console.log(response)
                const data = await response.json();
                console.log(data)
                setConfig(data);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        };
        fetchConfig();
    }, [configUrl]);

    return { config, loading, error };
};

export default useConfig;