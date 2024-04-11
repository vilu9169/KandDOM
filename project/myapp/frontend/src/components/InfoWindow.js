import { Container, Row, Col } from "react-bootstrap";
import { useRef, useEffect } from "react";
import { useContext } from "react";
import { showInfoWindowContext } from "./ShowInfoWindowContextProvider";
import timeLineLogo from "../assets/timeline.png";
import timeLineBorderLogo from "../assets/timeline_border.png";
import chatLogo from "../assets/chat.png";
import chatBorderLogo from "../assets/chat_border.png";
import folderLogo from "../assets/folder.png";
import pinLogo from "../assets/pin.png";
import pinArchiveLogo from "../assets/pin_archive.png";

console.log(timeLineLogo);

function InfoWindow() {
  const innerContainerRef = useRef(null);
  const { handleShowInfo } = useContext(showInfoWindowContext);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        innerContainerRef.current &&
        !innerContainerRef.current.contains(event.target)
      ) {
        handleShowInfo(); // Trigger the handleButtonClick function
      }
    };

    // Add event listener to detect clicks outside of the inner container
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [handleShowInfo]); // Include handleButtonClick in the dependency array
  return (
    <Container fluid className=" info-container">
      <Container ref={innerContainerRef} className="w-75 bg-2 info-window h-80">
        <Row className="h-10 bg-2 m-auto w-100 d-flex justify-content-center align-items-center">
          <h2 className="m-0">How to use Pythia?</h2>
        </Row>
        <Row className="h-80 bg-2 w-100 m-0 d-flex justify-content-center align-items-center">
          <Row className="h-25 bg-1 br-5 mb-2">
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-3 d-flex justify-content-center align-items-center">
                <img
                  className="p-0 m-0 w-75 h-75"
                  src={folderLogo}
                  alt="folderLogo"
                />
              </div>
            </Col>
            <Col className="col-10 h-100 bg-1 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">I.</span>
              <p className="p-0 m-0">
                <span className="bold">Document Upload:</span> Begin by
                uploading one or multiple PDF documents you wish to analyze.
                Simply click the "Add document" button in the top left corner of
                the screen. You can continue to add more documents as needed
                throughout your interaction.
              </p>
            </Col>
          </Row>
          <Row className="h-25 bg-3 m-2 br-5">
            <Col className="col-10 h-100 bg-3 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">II.</span>
              <p className="p-0 m-0">
                <span className="bold">Chatting with Pythia:</span> Engage with
                Pythia by asking questions or initiating conversations. You can
                type your queries directly into the chat interface and Pythia
                will provide relevant answers based on the content of the
                uploaded documents.
              </p>
            </Col>
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-1 d-flex justify-content-center align-items-center">
                <img
                  className="p-0 m-0 w-100 h-100"
                  src={chatLogo}
                  alt="chatLogo"
                />
              </div>
            </Col>
          </Row>
          <Row className="h-25 m-2 bg-1 br-5">
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-3 d-flex justify-content-center align-items-center">
                <img
                  className="p-0 m-0 w-100 h-100"
                  src={timeLineLogo}
                  alt="timeLineLogo"
                />
              </div>
            </Col>
            <Col className="col-10 h-100 bg-1 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">III.</span>
              <p className="p-0 m-0">
                <span className="bold">Timeline Analysis and Relation Graphs:</span> Explore the timeline feature to analyze chronological events
                within the documents. Additionally, delve into relationship
                graphs to uncover connections and associations between different
                elements within the content.
              </p>
            </Col>
          </Row>
          <Row className="h-25 m-2 bg-3 br-5">
            <Col className="col-10 h-100 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">IV.</span>
              <p className="p-0 m-0">
                <span className="bold">Archiving and Pinning:</span> Maintain an
                organized workflow by utilizing the archive and pin features.
                Pin important messages or insights displayed under the
                conversation for quick reference. Archive documents to keep
                track of your conversations and maintain an excellent workflow.
              </p>
            </Col>
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-1 d-flex justify-content-center align-items-center">
                <img
                  className="p-0 m-0 w-100 h-100"
                  src={pinArchiveLogo}
                  alt="pinArchiveLogo"
                />
              </div>
            </Col>
          </Row>
        </Row>
      </Container>
    </Container>
  );
}

export default InfoWindow;
