import { Container } from "react-bootstrap";
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
      <Container ref={innerContainerRef} className="d-flex info-window">
        <p className=" m-auto mx-5">
          Pythia is a tool to help you analyze legal documents quickly and efficiently.
          To get started please upload a PDF document you would like to analyze.
          You can upload a file by clicking the "Add document" button in the top left corner of the screen. 
          Pythia will then analyze the file and try to help you with your questions. 
          Pythia will answer questions about the document but will refrain from giving legal advice, passing judgement or making decisions.
          Pythia is trained on a large amount of data but may not be able to answer all questions, and all answers should be verified by a legal professional.
        </p>
      </Container>
        
    </Container>
  );
}

export default InfoWindow;