import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';
import SettingsMenu from './components/SettingsMenu'
import { AppProvider } from './components/ShowSettingsHandler';
import LogIn from './components/LogIn';
import Chatbot from './components/Chatbot';
import {MessageContextProvider} from './components/MessageContextProvider';
import {ResponseContextProvider} from './components/ResponseContextProvider';
import ContextProvider from './components/ContextProvider';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
      <Router>
       <ContextProvider>
      <Routes>
        <Route path='/' element={<PrivateRoute><Start/></PrivateRoute>} />
        <Route path='/login' element={<LogIn />} />
      </Routes>
      </ContextProvider>
      </Router>
  );
}

export default App;
