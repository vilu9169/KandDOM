import React, { useRef, useEffect, useContext } from "react";
import { Container } from "react-bootstrap";
import { Chrono } from "react-chrono";
import { AuthContext } from "./AuthContextProvider";


function TimeLine({ closeTimeline }) {
  const timelineContainerRef = useRef(null);
  const { timeLine } = useContext(AuthContext);

  useEffect(() => {
    const handleClickOutsideTimeLine = (event) => {
      if (
        timelineContainerRef.current &&
        !timelineContainerRef.current.contains(event.target)
      ) {
        closeTimeline();
      }
    };

    // Add event listener to detect clicks outside of the timeline container
    document.addEventListener("mousedown", handleClickOutsideTimeLine);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutsideTimeLine);
    };
  }, [closeTimeline]);
  return (
    <Container fluid className="info-container">
      <Container
        className="w-75 bg-2 info-window h-80"
        ref={timelineContainerRef}
      >
        <Chrono
          mode="VERTICAL"
          cardHeight="100"
          contentDetailsHeight="0"
          theme={{
            toolbarBgColor: "#f8f0e5",
            primary: "#dac0a3",
            secondary: "#f8f0e5",
            cardBgColor: "#f8f0e5",
            titleColor: "grey",
            titleColorActive: "black",
          }}
          items={timeLine}
        />
      </Container>
    </Container>
  );
}

export default TimeLine;
