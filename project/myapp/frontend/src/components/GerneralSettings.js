import { Button, Container, Row, Col, Form } from "react-bootstrap";
import { useContext, useState } from "react";
import { DarkModeContext } from "./DarkModeContextProvider";
import { alpha, styled } from '@mui/material/styles';
import Switch from '@mui/material/Switch';

const OurSwitch = styled(Switch)(({ theme }) => ({
  '& .MuiSwitch-switchBase.Mui-checked': {
    color: '#0f2c59',
    '&:hover': {
      backgroundColor: alpha('#0f2c59', theme.palette.action.hoverOpacity),
    },
  },
  '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
    backgroundColor: '#0f2c59',
  },
}));
function GeneralSettings() {
  const { isDarkMode, setIsDarkMode } = useContext(DarkModeContext);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode); // Use functional update to get the updated state value
    document.documentElement.classList.toggle("dark-mode");
    console.log(!isDarkMode); // Use !isDarkMode to get the updated value
  };
  return (
    <Container className="h-100">
      <Row className="p-3 d-flex align-items-center">
        <Col className="col-9 d-flex align-items-center">Dark Mode</Col>
        <Col className="col-3 d-flex justify-content-center align-items-center">
        <OurSwitch onClick={toggleDarkMode} checked={isDarkMode} size="small"/>
        </Col>
      </Row>
      <hr className="w-90 m-auto" />
      <Row className="p-3 d-flex align-items-center">
        <Col className="col-9 d-flex align-items-center">
          Ta bort alla chattar
        </Col>
        <Col className="col-3 d-flex justify-content-center align-items-center">
          <Button className=" btn-danger"> Ta bort</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default GeneralSettings;
