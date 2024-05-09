import { Button, Container, Row, Col } from "react-bootstrap";
import { IoIosDocument } from "react-icons/io";
import { useContext, useRef, useState, useEffect } from "react";
import { UploadWindowContext } from "./UploadWindowContextProvider";
import { AppContext } from "./ShowSettingsHandler";
import { useNavigate } from "react-router-dom";
import { FaLayerGroup } from "react-icons/fa";
import Fade from "react-bootstrap/Fade";
import { IoReturnUpBack } from "react-icons/io5";
import { AuthContext } from "./AuthContextProvider";
import { showInfoWindowContext } from "./ShowInfoWindowContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import { MessageContext } from "./MessageContextProvider";

function SideMenuTop({ uploadRef, clickedDocument, setClickedDocument }) {
function SideMenuTop({ uploadRef, clickedDocument, setClickedDocument }) {
  const { handleShowUploadWindow } = useContext(UploadWindowContext);
  const [isVisible, setIsVisible] = useState(false);
  const { handleButtonClick } = useContext(AppContext);
  const innerContainerRef = useRef(null);
  const personRef = useRef(null);
  const { setMessages } = useContext(ResponseContext);
  const { setMessage } = useContext(MessageContext);
  const { currentFile, setCurrentFile } = useContext(AuthContext);
  const navigate = useNavigate();
  const { logoutUser } = useContext(AuthContext);
  const { setCurrentGroup } = useContext(AuthContext);
  const { handleShowInfo } = useContext(showInfoWindowContext)
  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isVisible &&
        !personRef.current.contains(event.target) &&
        innerContainerRef.current &&
        !innerContainerRef.current.contains(event.target) //kan ta bort denna, försvinner ännu vid nästa knapptryck
      ) {
        toggleVisibility();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [toggleVisibility]);

  const backeToFiles = () => {
    setClickedDocument(false)
    setMessages([])
    setMessage('')
    setCurrentFile(null)
    setCurrentGroup(null)
  };

  return (
    <Container className="p-0">
      {clickedDocument ? (
        <Row className="w-90 m-sauto h-80px d-flex justify-content-center">
          <Col className="col-3 align-items-center d-flex justify-content-start">
            <Button
              onClick={() => 
                backeToFiles()
              }
              className="bg-3 rect-button align-items-center d-flex justify-content-center p-0"
            >
              <IoReturnUpBack className="size-20" />
            </Button>
          </Col>
          <Col className="col-9 pinned-text align-items-center d-flex justify-content-center">
            Pinned messages
          </Col>
        </Row>
      ) : (
        <>
          <div className="h-80px d-flex justify-content-center">
            <Button
              ref={personRef}
              onClick={toggleVisibility}
              className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
            >
              <span className="text-center justify-content-center d-flex align-items-center w-75">
                Add document
              </span>
              <span className="w-25 justify-content-center d-flex align-items-center">
                <IoIosDocument className="size-20" />
              </span>
            </Button>
          </div>
          <Fade
            mountOnEnter={true}
            unmountOnExit={true}
            appear={isVisible}
            in={isVisible}
          >
            <Container
              className="p-0 w-90 bg-1 user-pop-up-container"
              ref={innerContainerRef}
            >
              <Row className="p-0 m-0 h-50 w-100 ">
                <Button
                  onClick={() => handleShowUploadWindow(1)}
                  className="m-auto bg-3 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
                >
                  <span className="text-center justify-content-center d-flex align-items-center w-75">
                    Add to new chat
                  </span>
                  <span className="w-25 justify-content-center d-flex align-items-center">
                    <IoIosDocument className="size-20" />
                  </span>
                </Button>
              </Row>
              <Row className="p-0 m-0 h-50 w-100">
                {" "}
                <Button
                  onClick={() => handleShowUploadWindow(2)}
                  className="m-auto bg-3 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
                >
                  <span className="text-center justify-content-center d-flex align-items-center w-75">
                    Add to existing chat
                  </span>
                  <span className="w-25 justify-content-center d-flex align-items-center">
                    <FaLayerGroup className="size-20" />
                  </span>
                </Button>
              </Row>
            </Container>
          </Fade>
        </>
      )}
    </Container>
  );
}

export default SideMenuTop;
