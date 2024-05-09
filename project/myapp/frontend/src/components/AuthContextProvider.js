import { createContext, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import Cookies from 'js-cookie';
import axios from 'axios';
const AuthContext = createContext()

const AuthContextProvider = ({children}) => {
    let [user, setUser] = useState(() => (Cookies.get('access_token') ? jwtDecode(Cookies.get('access_token')).user : []))
    let [authTokens, setAuthTokens] = useState(() => (Cookies.get('access_tokens') ? JSON.parse(Cookies.get('access_token')) : null))
    let [loading, setLoading] = useState(true)
    let [loginError, setLoginError] = useState(null)
    let [signupError, setSignupError] = useState(null)
    let [userID, setUserID] = useState(() => (localStorage.getItem('userID') ? localStorage.getItem('userID') : null))
    const navigate = useNavigate()
    const [files, setFiles] = useState(localStorage.getItem('files') ? JSON.parse(localStorage.getItem('files')) : []);
    const [currentFile, setCurrentFile] = useState(localStorage.getItem('currentFile') ? localStorage.getItem('currentFile') : null);
    const [timeLine, setTimeLine] = useState([]);
    const [ docGroups, setDocGroups ] = useState(() => (localStorage.getItem('docGroups') ? JSON.parse(localStorage.getItem('docGroups')) : []));
    const [ currentGroup, setCurrentGroup ] = useState(() => (localStorage.getItem('currentGroup') ? localStorage.getItem('currentGroup') : null));

    const baseURL = process.env.REACT_APP_API_URL

    let getFiles = async (uID = null) => {
        const body = {
            user: uID ? uID : userID
        }
      try {
        const {data} = await axios.post(baseURL+"api/documents/", body);
        console.log(data.data);
        let fileArr = []
        for (const file of data.data) {
          console.log(file);
          fileArr.push(file);
        }
        setFiles(fileArr);
        localStorage.setItem('files', JSON.stringify(fileArr));
        console.log("Files:", files);
        getDocumentGroups();
        return data;
      }
      catch (error) {
        console.error("Error fetching files:", error);
      }
    };

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'   

    let getTimeLine = async (fileid) => {
        const body = {
            documentID: fileid
        }
        try {
            const {data} = await axios.post(baseURL+"api/get_timeline/", body);
            console.log(data);
            setTimeLine(data.timeline);
            console.log("TimeLine:", timeLine);
            return data;
        }
        catch (error) {
            console.error("Error fetching timeline:", error);
        }
    }

    let loginUser = async (e) => {
            e.preventDefault()
            console.log('username:', e.target.email.value)
            const body = {
                    email: e.target.email.value,
                    password: e.target.password.value
            }
            try {
                    const {data} = await axios.post(baseURL+"api/token/", body) // Updated URL to include the full address with the 'http://' protocol
                    console.log("data: ", data)
                    // Storing Access in cookie
                    Cookies.set('access_token', data.access);
                    Cookies.set('refresh_token', data.refresh);
                    setUser(jwtDecode(data.access).user)
                    setUserID(jwtDecode(data.access).user_id)
                    localStorage.setItem('userID', jwtDecode(data.access).user_id)
                    localStorage.setItem('currentFile', null)
                    localStorage.setItem('currentGroup', null)
                    console.log("decoded: ", jwtDecode(data.access).user)
                    navigate("/");
                    setLoginError(null)
                    setSignupError(null)
                    getFiles(jwtDecode(data.access).user_id)
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
            const response = await axios.post(baseURL+'api/signup/', body)
            console.log(response)
            loginUser(e)
        } catch (error) {
            setSignupError(error.response.data.detail)
            console.error('Error in signup:', error.response.data.detail)
        }
    }

    let getDocumentGroups = async () => {
        const body = {
            user: userID
        }
        try {
            const {data} = await axios.post(baseURL+"api/getDocGroups/", body);
            console.log(data.data);
            let fileArr = []
            for (const doc of data.data) {
              console.log(doc);
              fileArr.push(doc);
            }
            setDocGroups(fileArr);
            localStorage.setItem('docGroups', JSON.stringify(fileArr));
            console.log("docgroups:", files);
            return data;
          }
          catch (error) {
            console.error("Error fetching files:", error);
          }
    }

    let logoutUser = (e) => {
        e.preventDefault()
        Cookies.remove('access_token');
        Cookies.remove('refresh_token');
        localStorage.removeItem('userID')
        localStorage.removeItem('files')
        localStorage.removeItem('currentFile')
        localStorage.removeItem('messages')
        localStorage.removeItem('currentGroup')
        localStorage.removeItem('docGroups')
        localStorage.removeItem('pinnedMessages')
        localStorage.removeItem('timeLine')
        setAuthTokens(null)
        setUser(null)
        setUserID(null)
        setFiles([])
        setCurrentFile(null)
        setTimeLine([])
        setDocGroups([])
        setCurrentGroup(null)
        navigate('/login')
    }

    const updateToken = async () => {
        //http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/api/token/refresh/
        const response = await fetch(baseURL+'api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({refresh:authTokens?.refresh})
        })

        const data = await response.json()
        if (response.status === 200) {
            setAuthTokens(data)
            setUser(jwtDecode(data.access).user) // Add .user here
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
        files:files,
        signupError:signupError,
        currentFile:currentFile,
        timeLine:timeLine,
        docGroups:docGroups,
        currentGroup:currentGroup,
        setCurrentGroup:setCurrentGroup,
        getDocumentGroups:getDocumentGroups,
        setTimeLine:setTimeLine,
        setCurrentFile:setCurrentFile,
        getTimeLine:getTimeLine,
        getFiles:getFiles,
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
        setUser(access_token ? jwtDecode(access_token).user : null); // Add .user here
      }, [user]);

    return(
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}

export { AuthContext, AuthContextProvider}