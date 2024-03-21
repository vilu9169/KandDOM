import React, { useState } from "react";
import { Form } from "react-bootstrap";

function MyForm() {
    return (
    <Form className="w-100 d-flex justify-content-center">
    <Form.Control
      as="textarea"
      name="q"
      placeholder="Message Pythia..."
      className="h-50 w-75"
      autoComplete="off"
    ></Form.Control>
  </Form> 
  );
}

export default MyForm;
