import { Button, Container, Row } from "react-bootstrap";
import { IoIosDocument } from "react-icons/io";
import { useContext, useRef, useState, useEffect } from "react";
import { UploadWindowContext } from "./UploadWindowContextProvider";
import { AppContext } from "./ShowSettingsHandler";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import { FaLayerGroup } from "react-icons/fa";
import Fade from "react-bootstrap/Fade";

import { AuthContext } from "./AuthContextProvider";

function SideMenuTop() {
  const { handleShowUploadWindow } = useContext(UploadWindowContext);
  const [isVisible, setIsVisible] = useState(false);
  const { handleButtonClick } = useContext(AppContext);
  const innerContainerRef = useRef(null);
  const personRef = useRef(null);
  const navigate = useNavigate();
  const { logoutUser } = useContext(AuthContext);
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
        toggleVisibility(); // Trigger the handleButtonClick function
      }
    };

    // Add event listener to detect clicks outside of the inner container
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [toggleVisibility]);
  return (
    <Container className="p-0 position-absolute top-0 start-50 translate-middle-x mt-3">
      <Button
        ref={personRef}
        onClick={toggleVisibility}
        //onClick={handleShowUploadWindow}
        className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
      >
        <span className="text-center justify-content-center d-flex align-items-center w-75">
          Add document
        </span>
        <span className="w-25 justify-content-center d-flex align-items-center">
          <IoIosDocument className="size-20" />
        </span>
      </Button>
      <Fade
        mountOnEnter={true}
        unmountOnExit={true}
        appear={isVisible}
        in={isVisible}
      >
        <Container
          className="p-0 mt-3  w-90 bg-1 user-pop-up-container"
          ref={innerContainerRef}
        >
          <Row className="p-0 m-0 h-50 w-100 ">
            <Button
              onClick={handleShowUploadWindow}
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
              onClick={handleShowUploadWindow}
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
    </Container>
  );
}

export default SideMenuTop;
