import { Button, Container, Row, Col, Form } from "react-bootstrap";


function GeneralSettings() {
  return (
    <Container className="h-50">
      <Row className="h-50">
        <Col className="col-8 d-flex align-items-center">Dark Mode</Col>
        <Col className="col-4 d-flex justify-content-center align-items-center">
          <Form>
            <Form.Check type="switch" id="custom-switch" label=""></Form.Check>
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

