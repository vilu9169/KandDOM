import React from "react";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import { IoIosSend } from "react-icons/io";

function MyForm() {
  return (
    <Form className="w-100 h-100 d-flex justify-content-center">
      <InputGroup className="w-75 input-group-container">
        <Form.Control
          as="textarea"
          name="q"
          placeholder="Message Pythia..."
          autoComplete="off"
          className="input-textarea"
          style={{minHeight: 'unset'}}
        />
        <Button className="bg-3 message-button d-flex">
          <IoIosSend className="m-auto size-20"/>
        </Button>
      </InputGroup>
    </Form>
  );
}

export default MyForm;
