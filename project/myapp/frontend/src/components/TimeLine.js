import React, { useRef, useEffect } from "react";
import { Container } from "react-bootstrap";
import { Chrono } from "react-chrono";

function TimeLine({ closeTimeline }) {
  const timelineContainerRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        timelineContainerRef.current &&
        !timelineContainerRef.current.contains(event.target)
      ) {
        closeTimeline();
      }
    };

    // Add event listener to detect clicks outside of the timeline container
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [closeTimeline]);

  const items = [
    {
      title: "08/04/05, 14:20",
      cardTitle:
        "Engla försvinner på väg hem från Stjärnsund efter att ha varit och spelat fotboll.",
    },
    {
      title: "08/04/05, 19:45",
      cardTitle: "Anmälan om Englas försvinnande görs till polisen.",
    },
    {
      title: "08/04/06, 18:15",
      cardTitle: "Förundersökning inleds.",
    },
    {
      title: "08/04/07, 19:00",
      cardTitle: "Första förhör med den misstänkte, Per Anders Eklund, hålls.",
    },
    {
      title: "08/04/14, 09:22",
      cardTitle: "Primärrapporten om dödsfallet skrivs.",
    },
    {
      title: "08/04/14, 14:31",
      cardTitle: "Beslut om rättsmedicinsk obduktion fattas.",
      cardSubtitle:
        "On 10 May 1940, Hitler began his long-awaited offensive in the west...",
    },
    {
      title: "08/05/07, 15:40",
      cardTitle: "Beslut om hämtning av Eklund till förhör fattas.",
      cardDetailedText:
        "On 10 May 1940, Hitler began his long-awaited offensive in the west...",
    },
  ];

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
          items={items}
        />
      </Container>
    </Container>
  );
}

export default TimeLine;
