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
import { UploadWindowContext } from "./UploadWindowContextProvider";

function MyForm() {
  const {message, setMessage} = useContext(MessageContext);
  const {messages, setMessages} = useContext(ResponseContext);
  const {showUploadWindow } = useContext(UploadWindowContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const chatWithGPT3 = async () => {
    const apiEndpoint = baseURL+'/chat/';
    const headers = {
      'Content-Type': 'application/json',
    };
  
    // Extract only the text content from messages
    const messageTexts = messages.map(msg => ({ text: msg.text }));
  
    const data = {
      message: message,
      messages: messageTexts, // Stringify the array of message objects
    };
    
    console.log("Message texts:", messageTexts);
    console.log("Data sent to backend:", data); 
  
    try {
      const response = await axios.post(apiEndpoint, data, { headers });
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
      <InputGroup  className="w-75 input-group-container">
        <Form.Control
          disabled={showUploadWindow}
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
