import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';
import SettingsMenu from './components/SettingsMenu'
import { AppProvider } from './components/ShowSettingsHandler';
function App() {
  return (
   
      <Router>
        <AppProvider>
      <Routes>
        <Route index element={<Start/>} />
      </Routes>
      </AppProvider>
      </Router>
    
  );
}

export default App;
