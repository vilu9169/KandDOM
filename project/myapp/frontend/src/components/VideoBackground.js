import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import apolloLogo from "../assets/apollo.png";
import b_roll_1 from "../assets/videos/b_roll1.mp4";
import b_roll_2 from "../assets/videos/b_roll2.mp4";
import b_roll_3 from "../assets/videos/b_roll3.mp4";

const VideoBackground = () => {
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const videos = [b_roll_1, b_roll_2, b_roll_3];
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentVideoIndex((prevIndex) => (prevIndex + 1) % videos.length);
    }, 8000); // Change video every 5 seconds (adjust as needed)
    return () => clearInterval(interval);
  }, [videos]);

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100vh",
        overflow: "hidden",
      }}
    >
      {videos.map((video, index) => (
        <video
          key={index}
          src={video}
          autoPlay
          muted
          loop
          style={{
            left: 0,
            position: "absolute",
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: index === currentVideoIndex ? 1 : 0,
            transition: "opacity 1s ease",
          }}
        />
      ))}
      <Row className="video-header w-75 p-2">
        <Col className="col h-100 d-flex justify-content-center align-items-center">
          <h1 className="c-1 intro-text-big">Welcome to Pythia</h1>
          <img
            className="p-0 m-0 login-logo"
            src={apolloLogo}
            alt="apolloLogo"
          />
        </Col>
      </Row>
    </div>
  );
};

export default VideoBackground;
