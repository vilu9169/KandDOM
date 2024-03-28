import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";

function LogInLogic() {
  return (
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
  );
}

export default LogInLogic;
