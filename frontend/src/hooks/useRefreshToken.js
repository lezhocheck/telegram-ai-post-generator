import axios from '../api/axios';
import useAuth from './useAuth';

const useRefreshToken = () =>
{
    const { setAuth } = useAuth();

    const refresh = async () =>
    {
        const respose = await axios.post('/auth/refresh', {
            withCredentials: true
        });
        
        setAuth(prev =>
        {
            return { ...prev, token: respose.data.tokens.access };
        });

        return respose.data.tokens.access;
    }

    return refresh;
}

export default useRefreshToken;