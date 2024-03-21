import { FaUser } from "react-icons/fa";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { useContext, useRef, useState, useEffect } from "react";
import { IoIosSettings } from "react-icons/io";
import { IoIosLogOut } from "react-icons/io";
import { Transition } from "react-transition-group";
import { AppContext } from "./ShowSettingsHandler";
function SideMenuBottom() {
  const [isVisible, setIsVisible] = useState(false);
  const { handleButtonClick } = useContext(AppContext)
  const innerContainerRef = useRef(null)

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };


  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        isVisible &&
        innerContainerRef.current &&
        !innerContainerRef.current.contains(event.target)
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
    <Container className="position-relative">
      <Container className=" position-absolute bottom-0 start-50 translate-middle-x mb-3">
        <Transition in={isVisible} timeout={0}>
        {(isVisible) => <Container ref={innerContainerRef} style={{ transition:'opacity .2s ease-in-out', opacity: isVisible === 'entered' ? 1 : 0,}}>
            <ButtonGroup vertical className="w-100 bg-3 button-group-user">
              <Button onClick={handleButtonClick} className="settings-button ">
                <IoIosSettings size={25} className="settings-icon" />
                Settings
              </Button> 
              <Button className="logout-button">
                <IoIosLogOut size={25} className="logout-icon" />
                Log Out
              </Button>
            </ButtonGroup>
          </Container>}
        </Transition>
        <Button
          className="bg-1 border-0 text-black person-button"
          onClick={toggleVisibility}
        >
          {" "}
          <FaUser className="user-icon" /> Julius Amorm
        </Button>
      </Container>

    </Container>
    
  );
}

export default SideMenuBottom;
