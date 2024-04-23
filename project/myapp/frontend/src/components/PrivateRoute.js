import { Navigate } from 'react-router-dom'
import { useContext, useState } from 'react'
import { AuthContext } from './AuthContextProvider'

const PrivateRoute = ({children}) => {
    const { user } = useContext(AuthContext)

    return !user ? <Navigate to='/login'/> : children;
}

export default PrivateRoute;