import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import MyForm from "./Form";
import UploadFileWindow from "./UploadFileWindow"
import { IoMdHelp } from "react-icons/io";


function Start() {
  return (
    <Container fluid className="position-absolute h-100 text-center bg-3">
      <Row className="h-100">
        <Col className="col-2">
          <Row className="h-75 bg-2">apa</Row>
          <Row className="h-25  bg-2">xd</Row>
        </Col>
        <Col className="col-10 d-flex flex-column">
          <Row className="h-60px bg-3">
            <Row className="h-100 bg-1 m-auto">
              <Col className="col-6 h-100 bg-1 align-items-end d-flex justify-content-start">
                <h2 className="p-0 m-0">Pythia</h2>
                {/* Add company icon */ }
              </Col>
              <Col className="col-6 h-100 d-flex align-items-end justify-content-end">
                <Button className="bg-3 rect-button align-items-center d-flex justify-content-center p-0">
                <IoMdHelp className="size-20" />

                </Button>
              </Col>
            </Row>
          </Row>
          <Row className="flex-grow-1 bg-1">
            <UploadFileWindow></UploadFileWindow>
          
          </Row>
          <Row className="h-80px bg-1 align-items-top">
            <MyForm></MyForm>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default Start;
