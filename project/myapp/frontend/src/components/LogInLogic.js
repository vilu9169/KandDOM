import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import { IoIosLogIn } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import { useContext } from "react";

function LogInLogic({ onSignUpClick }) {
  let {loginUser} = useContext(AuthContext)
  return (
    <Form className="m-auto h-100" onSubmit={ loginUser }>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <h2 className="p-0 m-0">Welcome Back!</h2>
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Form.Control
          className="w-75 input-group-container"
          autoComplete={false}
          type="email"
          placeholder="Email"
        />
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Form.Control
          className="w-75 input-group-container"
          type="password"
          placeholder="Password"
        />
        {/* <Form.Text className="ms-3 w-25">Glömt lösenord?</Form.Text>*/}
      </Row>
      <Row className="h-25 bg-1 m-auto w-100 d-flex justify-content-center align-items-center">
        <Button
          className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
          href="/"
        >
          <span className="text-center justify-content-center d-flex align-items-center w-75">
            Log in
          </span>
          <span className="w-25 justify-content-center d-flex align-items-center">
            <IoIosLogIn className="size-20" />
          </span>
        </Button>
        <Form.Text className="w-90">
          Don't have an account?{" "}
          <span onClick={onSignUpClick} className="click-text">
            Sign Up
          </span>
        </Form.Text>
      </Row>
    </Form>
  );
}

export default LogInLogic;
