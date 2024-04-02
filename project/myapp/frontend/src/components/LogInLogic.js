import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import { useContext } from "react";
import { AuthContext } from "./AuthContextProvider";

function LogInLogic() {
  let {loginUser} = useContext(AuthContext)

  return (
    <Form className="m-auto" onSubmit={ loginUser }>
      <FormGroup className="m-auto text-start login-group w-50">
        <Form.Control
          className="my-5 login-form"
          name="username"
          autoComplete={false}
          type="username"
          placeholder="Enter username"
        />
        <Form.Control
          name="password"
          className=" mt-5 login-form"
          type="password"
          placeholder="Password"
        />
        <Form.Text className="ms-3">Glömt lösenord?</Form.Text>
      </FormGroup>
      <Button type="submit" className="bg-4 border-0 mt-3" href="/">
        Login
      </Button>
    </Form>
  );
}

export default LogInLogic;
