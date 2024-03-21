import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Routes, Route, BrowserRouter } from "react-router-dom";
import Start from './components/start';

function App() {
  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route index element={<Start/>} />
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
