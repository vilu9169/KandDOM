import { FaUser } from "react-icons/fa";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { useContext, useRef, useState, useEffect } from "react";
import { IoIosSettings } from "react-icons/io";
import { IoIosLogOut } from "react-icons/io";
import { IoMdPerson } from "react-icons/io";

import Row from "react-bootstrap/Row";
import { Transition } from "react-transition-group";
import { AppContext } from "./ShowSettingsHandler";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import LogIn from "./LogIn";

import Collapse from "react-bootstrap/Collapse";
import Fade from "react-bootstrap/Fade";
function SideMenuBottom() {
  const [isVisible, setIsVisible] = useState(false);
  const { handleButtonClick } = useContext(AppContext);
  const innerContainerRef = useRef(null);
  const personRef = useRef(null);
  const navigate = useNavigate();

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const handleLogout = () => {
    // Perform logout actions here
    // For example, clear local storage, reset user state, etc.
    // Then navigate to the login page
    navigate("/login");
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
  }, [toggleVisibility]); // Include handleButtonClick in the dependency array

  return (
      <Container className="p-0 m-0 position-absolute bottom-0 start-50 translate-middle-x mb-3">
        <Fade in={isVisible}>
          <Container
            className="p-0 w-90 bg-1 user-pop-up-container"
            ref={innerContainerRef}
          >
            <Row className="p-0 m-0 h-50 w-100 ">
              <Button
                onClick={handleButtonClick}
                className="m-auto bg-1 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
              >
                <span className="text-center justify-content-center d-flex align-items-center w-75">
                  Settings
                </span>
                <span className="w-25 justify-content-center d-flex align-items-center">
                  <IoIosSettings className="size-20" />
                </span>
              </Button>
            </Row>
            <Row className="p-0 m-0 h-50 w-100">
              {" "}
              <Button
                onClick={handleLogout}
                className="m-auto bg-1 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
              >
                <span className="text-center justify-content-center d-flex align-items-center w-75">
                  Log Out
                </span>
                <span className="w-25 justify-content-center d-flex align-items-center">
                  <IoIosLogOut className="size-20" />
                </span>
              </Button>
            </Row>
          </Container>
        </Fade>
        <Button
          ref={personRef}
          onClick={toggleVisibility}
          className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
        >
          <span className="text-center justify-content-center d-flex align-items-center w-75">
            Julius amorm
          </span>
          <span className="w-25 justify-content-center d-flex align-items-center">
            <IoMdPerson className="size-20" />
          </span>
        </Button>
      </Container>
  );
}

export default SideMenuBottom;
