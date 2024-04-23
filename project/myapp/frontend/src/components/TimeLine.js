import { Container } from "react-bootstrap";
import { Chrono } from "react-chrono";
//import "react-chrono/dist/styles.css";

function TimeLine() {
  const items = [
    {
      title: "May 24, 1940",
      cardTitle: "Dunkirk",
      cardSubtitle:
        "Men of the British Expeditionary Force (BEF) wade out to a destroyer during the evacuation from Dunkirk.",
      cardDetailedText:
        "On 10 May 1940, Hitler began his long-awaited offensive in the west...",
    },
    {
      title: "May 1945",
      cardTitle: "sdfsdafd",
      cardSubtitle:
        "Men of the British Expeditionary Force (BEF) wade out to a destroyer during the evacuation from Dunkirk.",
      cardDetailedText:
        "On 10 May 1940, Hitler began his long-awaited offensive in the west...",
    },
  ];
  return (
    <Container fluid className="info-container">
      <Container className="w-75 bg-2 info-window h-80">
        <Chrono
          mode="HORIZONTAL"
          theme={{
            //toolbarBtnBgColor: '#eadbc8',
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
