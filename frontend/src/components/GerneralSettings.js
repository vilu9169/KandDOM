import { Button, Container, Row, Col, Form } from "react-bootstrap";


function GeneralSettings() {
    return (
        <Container className=" h-100">
            <Row className=" pb-5 border-bottom mt-5">
                <Col className=" text-start">
                Dark Mode
                </Col>
                <Col>
                    <Form className=" d-flex justify-content-end">
                        <Form.Check
                        
                        type="switch"
                        id="custom-switch"
                        label="">

                        </Form.Check>
                    </Form>
                </Col>
            </Row>
            <Row className="mt-5">
                <Col className="text-start">
                Ta bort alla chattar
                </Col>
                <Col className=" d-flex justify-content-end">
                <Button className=" btn-danger"> Ta bort</Button>
                </Col>
            </Row>
        </Container>
    );
}

export default GeneralSettings;