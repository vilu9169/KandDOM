import React from "react";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import { IoIosSend } from "react-icons/io";
import { useContext } from "react";
import { MessageContext } from "./MessageContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import axios from "axios";
import { useRef } from "react";

function MyForm() {
  const {message, setMessage} = useContext(MessageContext);
  const {messages, setMessages} = useContext(ResponseContext);
const chatWithGPT3 = async (userInput) => {
  const apiEndpoint = 'http://127.0.0.1:8000/chat/';
  const headers = {
    'Content-Type': 'application/json',
  };

  const data = {
    message
  };
try {
    const response = await axios.post(apiEndpoint, data);
    return response.data.message;
  } catch (error) {
    console.error('Error communicating with the API:', error.message);
    return '';
  }
};
const handleSubmit = async (e) => {
  e.preventDefault();
  const userMessage = { text: message, user: true };
  setMessages((prevMessages) => [...prevMessages, userMessage]);
  const aiMessage = { text: '...', user: false };
  setMessages((prevMessages) => [...prevMessages, aiMessage]);
  const response = await chatWithGPT3(message);
  const newAiMessage = { text: response, user: false };
  setMessages((prevMessages) => [...prevMessages.slice(0, -1), newAiMessage]);
  setMessage();
};
const handleMessageChange = (event) => {
  setMessage(event.target.value);
};
const form = useRef();

function handleKeyUp(event) {
  // Enter
  if (event.keyCode === 13) {
    handleSubmit(event);
    form.current.reset();
  }
}
  return (
    <Form ref={form} onKeyUp={handleKeyUp} className="w-100 h-100 d-flex justify-content-center">
      <InputGroup className="w-75 input-group-container">
        <Form.Control
          as="textarea"
          name="q"
          placeholder="Message Pythia..."
          autoComplete="off"
          className="input-textarea"
          style={{minHeight: 'unset'}}
          onChange={handleMessageChange}
          onSubmit={handleSubmit}
        />
        <Button onClick={handleSubmit} className="bg-3 message-button d-flex">
          <IoIosSend className="m-auto size-20"/>
        </Button>
      </InputGroup>
    </Form>
  );
}

export default MyForm;
