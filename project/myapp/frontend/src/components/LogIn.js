import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import VideoBackground from "./VideoBackground";
import Start from "./start";
import { IoIosLogIn } from "react-icons/io";

import { useState } from "react";
import LogInLogic from "./LogInLogic";
import SignUpLogic from "./SignUpLogic";

function LogIn() {
  const videos = [
    "../assets/videos/b_roll1.mp4",
    "../assets/videos/b_roll2.mp4",
    "../assets/videos/b_roll3.mp4",
  ];

  const [showLogInForm, setShowLogInForm] = useState(false);
  const [showSignUpForm, setShowSignUpForm] = useState(false);

  const handleLoginClick = () => {
    setShowLogInForm(true);
    setShowSignUpForm(false);
  };

  const handleSignUpClick = () => {
    setShowSignUpForm(true);
    setShowLogInForm(false);
  };

  return (
    <Container fluid className=" text-center login-container">
      <Row className="h-100">
        <Col className="col image-column m-0 p-0">
          <VideoBackground videos={videos} />
        </Col>
        <Col className="col bg-2 login-column">
          <Row className="h-100 align-items-center d-flex justify-content-center">
            <Container className="w-75 h-60 bg-1 br-5">
              {showLogInForm ? (
                <LogInLogic onSignUpClick={handleSignUpClick}/>
              ) : showSignUpForm ? (
                <SignUpLogic onLoginClick={handleLoginClick}/>
              ) : (
                <>
                  <Row className="h-50 d-flex align-items-center">
                    <h2 className="p-0 m-0">Get started</h2>
                  </Row>
                  <Row className="h-50 justify-content-center d-flex align-items-center">
                    <Row className="h-50">
                      <Button
                        className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
                        onClick={handleLoginClick}
                      >
                        <span className="text-center justify-content-center d-flex align-items-center w-75">
                          Log in
                        </span>
                        <span className="w-25 justify-content-center d-flex align-items-center">
                          <IoIosLogIn className="size-20" />
                        </span>
                      </Button>
                    </Row>
                    <Row className="h-50">
                      <Button
                        className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
                        onClick={handleSignUpClick}
                      >
                        <span className="text-center justify-content-center d-flex align-items-center w-100">
                          Sign up
                        </span>
                      </Button>
                    </Row>
                  </Row>
                </>
              )}
            </Container>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default LogIn;
