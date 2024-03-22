import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import VideoBackground from "./VideoBackground";
import Start from "./start";
function LogIn() {
  const videos = [
    "videos/b_roll1.mp4",
    "videos/b_roll2.mp4",
    "videos/b_roll3.mp4",
  ];
  return (
    <Container fluid className=" text-center login-container">
      <Row className="h-100">
        <Col className=" col-8 image-column m-0 p-0">
          <VideoBackground videos={videos} />
        </Col>
        <Col className=" col-4 login-column h-100">
          <Row className="h-100">
            <Form className="m-auto">
              <FormGroup className="m-auto text-start login-group w-50">
                <Form.Control
                  className="my-5 login-form"
                  autoComplete={false}
                  type="email"
                  placeholder="Enter email"
                />
                <Form.Control
                  className=" mt-5 login-form"
                  type="password"
                  placeholder="Password"
                />
                <Form.Text className="ms-3">Glömt lösenord?</Form.Text>
              </FormGroup>
              <Button className="bg-4 border-0 mt-3" href="/">
                Login
              </Button>
            </Form>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default LogIn;
