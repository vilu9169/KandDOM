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
import { AuthContext } from "./AuthContextProvider";
import { TbTimelineEventFilled } from "react-icons/tb";
import TimeLine from "./TimeLine";

function SideMenuBottom({ clickedDocument, showTimeline, setShowTimeline }) {
  const [isVisible, setIsVisible] = useState(false);
  const { handleButtonClick } = useContext(AppContext);
  const innerContainerRef = useRef(null);
  const personRef = useRef(null);
  const navigate = useNavigate();
  const { logoutUser } = useContext(AuthContext);
  const { user } = useContext(AuthContext);

  const [userName] = useState(user.name);

  const handleTimelineButtonClick = () => {
    setShowTimeline(!showTimeline);
  };

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
  }, [toggleVisibility]); // Include handleButtonClick in the dependency array

  return (
    <Container className="p-0 m-0 position-absolute bottom-0 start-50 translate-middle-x mb-3">
      {clickedDocument && (
        <Button
          onClick={() => setShowTimeline(!showTimeline)}
          className="m-auto mb-3 bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
        >
          <span className="text-center justify-content-center d-flex align-items-center w-75">
            Timeline
          </span>
          <span className="w-25 justify-content-center d-flex align-items-center">
            <TbTimelineEventFilled className="size-20" />
          </span>
        </Button>
      )}

      <Fade
        mountOnEnter={true}
        unmountOnExit={true}
        appear={isVisible}
        in={isVisible}
      >
        <Container
          className="p-0 mb-2  w-90 bg-1 user-pop-up-container"
          ref={innerContainerRef}
        >
          <Row className="p-0 m-0 h-50 w-100 ">
            <Button
              onClick={handleButtonClick}
              className="m-auto bg-3 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
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
              onClick={logoutUser}
              className="m-auto bg-3 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
            >
              <span className="small text-center justify-content-center d-flex align-items-center w-75">
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
          {userName}
        </span>
        <span className="w-25 justify-content-center d-flex align-items-center">
          <IoMdPerson className="size-20" />
        </span>
      </Button>
    </Container>
  );
}

export default SideMenuBottom;
