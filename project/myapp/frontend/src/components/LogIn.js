import { Button, Col, Container, FormGroup, Row, Form } from "react-bootstrap";
import VideoBackground from "./VideoBackground";
import Start from "./start";
import { IoIosLogIn } from "react-icons/io";

import { useState } from "react";
import LogInLogic from "./LogInLogic";

function LogIn() {
  const videos = [
    "videos/b_roll1.mp4",
    "videos/b_roll2.mp4",
    "videos/b_roll3.mp4",
  ];
  const [showLoginForm, setShowLoginForm] = useState(false);

  const handleLoginClick = () => {
    setShowLoginForm(true);
  };

  return (
    <Container fluid className=" text-center login-container">
      <Row className="h-100">
        <Col className=" col-8 image-column m-0 p-0">
          <VideoBackground videos={videos} />
        </Col>
        <Col className=" col-4 bg-2 login-column h-100">
          <Row className="h-100 align-items-center d-flex justify-content-center">
            <Container className="w-75 h-50 bg-1 br-5">
              {showLoginForm ? (
                <LogInLogic></LogInLogic>
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
                        href="/"
                        className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
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
