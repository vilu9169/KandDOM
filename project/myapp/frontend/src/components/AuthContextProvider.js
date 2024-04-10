import { createContext, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Cookies from 'js-cookie';
import axios from 'axios';
const AuthContext = createContext()


const AuthContextProvider = ({children}) => {
    let [user, setUser] = useState(() => (Cookies.get('access_token') ? jwtDecode(Cookies.get('access_token')) : null))
    let [authTokens, setAuthTokens] = useState(() => (Cookies.get('access_tokens') ? JSON.parse(Cookies.get('access_token')) : null))
    let [loading, setLoading] = useState(true)
    let [loginError, setLoginError] = useState(null)
    let [signupError, setSignupError] = useState(null)
    let [userID, setUserID] = useState(() => (localStorage.getItem('userID') ? jwtDecode(Cookies.get('access_token')).user_id : null))
    const navigate = useNavigate()

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

    let loginUser = async (e) => {
            e.preventDefault()
            console.log('username:', e.target.email.value)
            const body = {
                    email: e.target.email.value,
                    password: e.target.password.value
            }
            try {
                    const {data} = await axios.post("http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/api/token/", body) // Updated URL to include the full address with the 'http://' protocol
                    console.log("data: ", data)
                    // Storing Access in cookie
                    Cookies.set('access_token', data.access);
                    Cookies.set('refresh_token', data.refresh);
                    setUser(jwtDecode(data.access).email)
                    setUserID(jwtDecode(data.access).user_id)
                    localStorage.setItem('userID', jwtDecode(data.access).user_id)
                    navigate("/");
                    setLoginError(null)
                    setSignupError(null)
                } catch (error) {
                    setLoginError(error.response.data.detail)
                    console.log(error.response.data.detail)
                    console.error("error in token fetch: ", error.message)
                }

    }

    let signupUser = async (e) => {
        e.preventDefault()
        const body = {
            email: e.target.email.value,
            password: e.target.password.value,
            name: e.target.name.value
        }

        try {
            const response = await axios.post('http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/api/signup/', body)
            console.log(response)
            loginUser(e)
        } catch (error) {
            setSignupError(error.response.data.detail)
            console.error('Error in signup:', error.response.data.detail)
        }
    }


    let logoutUser = (e) => {
        e.preventDefault()
        Cookies.remove('access_token');
        Cookies.remove('refresh_token');
        localStorage.removeItem('userID')
        setAuthTokens(null)
        setUser(null)
        navigate('/login')
    }

    const updateToken = async () => {
        const response = await fetch('1http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({refresh:authTokens?.refresh})
        })

        const data = await response.json()
        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            Cookies.set('access_token',JSON.stringify(data))
        } else {
            logoutUser()
        }

        if(loading){
            setLoading(false)
        }
    }

    let contextData = {
        user:user,
        userID:userID,
        authTokens:authTokens,
        loginError:loginError,
        signupError:signupError,
        loginUser:loginUser,
        logoutUser:logoutUser,
        signupUser:signupUser,
    }

    useEffect(()=>{
        const REFRESH_INTERVAL = 1000 * 60 * 4 // 4 minutes
        let interval = setInterval(()=>{
            if(authTokens){
                updateToken()
            }
        }, REFRESH_INTERVAL)
        return () => clearInterval(interval)

    },[authTokens])
    useEffect(() => {
        const access_token = Cookies.get('access_token');
        setUser(access_token ? jwtDecode(access_token) : null);
      }, [user]);

    return(
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}

export { AuthContext, AuthContextProvider}