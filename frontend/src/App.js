import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';
import SettingsMenu from './components/SettingsMenu'
import { AppProvider } from './components/ShowSettingsHandler';
import LogIn from './components/LogIn';
import Chatbot from './Chatbot';
function App() {
  return (
      <Router>
        <AppProvider>
      <Routes>
        <Route index element={<Start/>} />
        <Route path='/login' element={<LogIn />} />
        <Route path='/chat' element={<Chatbot/>}></Route>
      </Routes>
      </AppProvider>
      </Router>
  );
}

export default App;
