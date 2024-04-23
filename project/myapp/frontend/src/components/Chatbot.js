import React, { useContext, useRef, useEffect } from "react";
import { ResponseContext } from "./ResponseContextProvider";
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css"; // Import Perfect Scrollbar CSS
import apolloLogo from "../assets/apollo.png";
import pinLogo from "../assets/pin.png";
import { Container, Row, Col } from "react-bootstrap";
import { TiPin } from "react-icons/ti";
import ChatMessage from './ChatMessage';
import { TiPinOutline } from "react-icons/ti";
const Chatbot = () => {
  const { messages } = useContext(ResponseContext);
  const chatWindowRef = useRef(null);
  let ps;

  useEffect(() => {
    if (chatWindowRef.current) {
      ps = new PerfectScrollbar(chatWindowRef.current, {
        wheelPropagation: true, // Example option, you can add more options here
      });
    }

    scrollToBottom();

    return () => {
      if (ps) {
        ps.destroy();
      }
    };
  }, []); // Only initialize PerfectScrollbar once on component mount

  useEffect(() => {
    updateScrollbar();
  }, [messages]); // Update scrollbar whenever messages change

  const updateScrollbar = () => {
    scrollToBottom(); // Scroll to bottom
  };

  const scrollToBottom = () => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight; // Set scroll position to bottom
    }
  };

  return (
    <Container className="chatbot-container" ref={chatWindowRef}>
      <Container className="chatbot-messages w-100 p-0">
        {messages.map((message, index) => (
          <Container
            key={index}
            className={`message ${
              message.user ? "user-message" : "ai-message"
            } w-100 `}
          >
            <Row className="w-100">
              <Col className="col w-50px d-flex justify-content-center align-items-center">
                <img
                  className="p-0 m-0 chat-logo"
                  src={message.user ? pinLogo : apolloLogo}
                  alt="chatLogo"
                />
              </Col>
              <Col className="col d-flex align-items-center">
                <p className="m-0 user-text">
                  {message.user ? "You" : "Pythia"}
                </p>
              </Col>
            </Row>
            <Row className="w-100">
              <p className="message-text"><ChatMessage text={message.text} /></p>
            </Row>
            <Row className="d-flex justify-content-start w-100 h-20px">
              <TiPin className="m-0 p-0" />
            </Row>
          </Container>
        ))}
      </Container>
    </Container>
  );
};

export default Chatbot;
