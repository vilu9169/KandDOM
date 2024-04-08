import { Container, Row, Col } from "react-bootstrap";
import { useRef, useEffect } from "react";
import { useContext } from "react";
import { showInfoWindowContext } from "./ShowInfoWindowContextProvider";
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
      <Container ref={innerContainerRef} className="w-50 bg-2 info-window h-80">
        <Row className="h-10 bg-2 m-auto w-100 d-flex justify-content-center align-items-center">
          <h2 className="m-0">How to use Pythia?</h2>
        </Row>
        <Row className="h-80 bg-2 w-100 m-0 d-flex justify-content-center align-items-center">
          <Row className="h-25 bg-1 br-5 mb-2">
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-3 d-flex justify-content-center align-items-center">
                asdasd
              </div>
            </Col>
            <Col className="col-10 h-100 bg-1 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">I.</span>
              To get started please upload one or multiple PDF documents you
              would like to analyze. You can upload a by clicking the "Add
              document" button in the top left corner of the screen.
            </Col>
          </Row>
          <Row className="h-25 bg-3 m-2 br-5">
            <Col className="col-10 h-100 bg-3 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">II.</span>
              You can always add additional dokuments to your chats by clicking the same button.
            </Col>
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-1 d-flex justify-content-center align-items-center">
                asdasd
              </div>
            </Col>
          </Row>
          <Row className="h-25 m-2 bg-1 br-5">
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-3 d-flex justify-content-center align-items-center">
                asdasd
              </div>
            </Col>
            <Col className="col-10 h-100 bg-1 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">III.</span>
              Now you can start asking question, analyse the timeline or dive deeper into the realations that appear in the pdf. 
              Remember that Pythia will answer questions about the document but will refrain
              from giving legal advice, passing judgement or making decisions.
            </Col>
          </Row>
          <Row className="h-25 m-2 bg-3 br-5">
            <Col className="col-10 h-100 d-flex justify-content-center align-items-center">
              <span className="big-roman m-3">IV.</span>
              Finally use pin(displayed under conversation) aswell as archive(displayed when hovering document in sidebar) to keep track of your convos and keep a exellent workflow.
            </Col>
            <Col className="col-2 h-100 d-flex justify-content-center align-items-center p-0">
              <div className="circle bg-1 d-flex justify-content-center align-items-center">
                asdasd
              </div>
            </Col>
          </Row>
        </Row>
      </Container>
    </Container>
  );
}

export default InfoWindow;
