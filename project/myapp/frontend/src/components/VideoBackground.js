import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const VideoBackground = ({ videos }) => {
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentVideoIndex((prevIndex) => (prevIndex + 1) % videos.length);
    }, 8000); // Change video every 5 seconds (adjust as needed)
    return () => clearInterval(interval);
  }, [videos]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh', overflow: 'hidden' }}>
      {videos.map((video, index) => (
        <video
          key={index}
          src={video}
          autoPlay
          muted
          loop
          style={{
            left:0,
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: index === currentVideoIndex ? 1 : 0,
            transition: 'opacity 1s ease',
          }}
        />
      ))}
      <Container className='video-header'>
        <Row>
          <Col>
            {/* Your content goes here */}
            <h1>Welcome to Pythia</h1>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default VideoBackground;