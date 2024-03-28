import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';
import SettingsMenu from './components/SettingsMenu'
import { AppProvider } from './components/ShowSettingsHandler';
import LogIn from './components/LogIn';
function App() {
  return (
   
      <Router>
        <AppProvider>
      <Routes>
        <Route index element={<Start/>} />
        <Route path='/login' element={<LogIn />} />
      </Routes>
      </AppProvider>
      </Router>
    
  );
}

export default App;
