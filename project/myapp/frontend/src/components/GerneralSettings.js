import { Button, Container, Row, Col, Form } from "react-bootstrap";
import { useContext, useState } from "react";
import { DarkModeContext } from "./DarkModeContextProvider";

function GeneralSettings() {
  const { isDarkMode, setIsDarkMode } = useContext(DarkModeContext);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode); // Use functional update to get the updated state value
    document.documentElement.classList.toggle("dark-mode");
    console.log(!isDarkMode); // Use !isDarkMode to get the updated value
  };
  return (
    <Container className="h-50">
      <Row className="h-50">
        <Col className="col-8 d-flex align-items-center">Dark Mode</Col>
        <Col className="col-4 d-flex justify-content-center align-items-center">
          <Form>
            <Form.Check
              checked={isDarkMode}
              type="switch"
              onClick={toggleDarkMode}
              id="custom-switch"
              label=""
            ></Form.Check>
          </Form>
        </Col>
      </Row>
      <Row className="h-50">
        <Col className="col-8 d-flex align-items-center">
          Ta bort alla chattar
        </Col>
        <Col className="col-4 d-flex justify-content-center align-items-center">
          <Button className=" btn-danger"> Ta bort</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default GeneralSettings;
