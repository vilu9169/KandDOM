import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import { IoIosLogIn } from "react-icons/io";

function SignUpLogic({ onLoginClick }) {
  return (
    <Form className="m-auto h-100">
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <h2 className="p-0 m-0">Create an account</h2>
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Form.Control
          className="w-75 input-group-container"
          autoComplete={false}
          type="email"
          placeholder="Email"
          name = "email"
        />
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Form.Control
          className="w-75 input-group-container"
          type="password"
          placeholder="Password"
          name="password"
        />
        {/* <Form.Text className="ms-3 w-25">Glömt lösenord?</Form.Text>*/}
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Button type="submit" className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1">
          <span className="text-center justify-content-center d-flex align-items-center w-100">
            Sign up
          </span>
        </Button>
        <Form.Text className="w-90">
          Already have an account?{" "}
          <span onClick={onLoginClick} className="click-text">
            Login
          </span>
        </Form.Text>
      </Row>
    </Form>
  );
}

export default SignUpLogic;
