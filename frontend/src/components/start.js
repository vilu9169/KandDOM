import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosSend } from "react-icons/io";
import MyForm from "./Form";

function Start() {
  return (
    <Container fluid className="position-absolute h-100 text-center bg-3">
      <Row className="h-100">
        <Col color="" className="col-2">
          <Row className="h-75 bg-2">apa</Row>
          <Row className="h-25  bg-2">xd</Row>
        </Col>
        <Col className="col-10">
          <Row className="h-10 bg-3">jsjd</Row>
          <Row className="h-80 bg-1">jsjd</Row>
          <Row className="h-10 bg-1 align-items-top">
            <MyForm></MyForm>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default Start;
