import React, { useContext, useRef, useEffect } from "react";
import { ResponseContext } from "./ResponseContextProvider";
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css"; // Import Perfect Scrollbar CSS
import apolloLogo from "../assets/apollo.png";
import { Container } from "react-bootstrap";

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
    <div className="chatbot-container" ref={chatWindowRef}>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <Container>
          <Row>
            <Col className=""></Col>
            <Col></Col>
          </Row>
          <Row>

          </Row>
          </Container>
          /*   
          <div
            key={index}
            className={`message ${
              message.user ? "user-message" : "ai-message"
            }`}
          >
            <img
              className="p-0 m-0 chat-logo"
              src={apolloLogo}
              alt="apolloLogo"
            />
            <p className="user-text">{message.user ? "You" : "Pythia"}</p>
            <p className="message-text">{message.text}</p>
          </div>*/
        ))}
      </div>
    </div>
  );
};

export default Chatbot;
