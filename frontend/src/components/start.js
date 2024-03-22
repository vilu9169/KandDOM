import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosSend } from "react-icons/io";
import MyForm from "./Form";
import SideMenuBottom from "./SideMenuBottom";
import SettingsMenu from "./SettingsMenu";
import { useContext, useState } from "react";
import { AppContext } from "./ShowSettingsHandler";
import SideMenuTop from "./SideMenuTop";
function Start() {
  const { buttonClicked } = useContext(AppContext);

  return (
    <Container fluid className="position-absolute h-100 text-center bg-3">
      <Row className="h-100">
        <Col color="" className="col-2 sidemenu">
          <Row className="h-75 bg-2 position-relative">
            <SideMenuTop />
          </Row>
          <Row className="h-25  bg-2">
            <SideMenuBottom />
          </Row>
        </Col>
        <Col className="col-10">
          <Row className="h-10 bg-3">jsjd</Row>
          <Row className="h-80 bg-1">jsjd</Row>
          <Row className="h-10 bg-1 align-items-top">
            <MyForm></MyForm>
          </Row>
        </Col>
      </Row>
      {buttonClicked && <SettingsMenu />}
    </Container>
  );
}

export default Start;
