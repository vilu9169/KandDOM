import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';
import SettingsMenu from './components/SettingsMenu'
import { AppProvider } from './components/ShowSettingsHandler';
import LogIn from './components/LogIn';
import Chatbot from './components/Chatbot';
import {MessageContextProvider} from './components/MessageContextProvider';
import {ResponseContextProvider} from './components/ResponseContextProvider';

function App() {
  return (
      <Router>
        <ResponseContextProvider>
        <MessageContextProvider>
        <AppProvider>
      <Routes>
        <Route index element={<Start/>} />
        <Route path='/login' element={<LogIn />} />
      </Routes>
      </AppProvider>
      </MessageContextProvider>
      </ResponseContextProvider>
      </Router>
  );
}

export default App;
