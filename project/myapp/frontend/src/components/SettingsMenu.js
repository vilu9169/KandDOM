import { Container, Button, ButtonGroup } from "react-bootstrap";
import { AppContext } from "./ShowSettingsHandler";
import { useContext, useEffect, useRef, useState } from "react";
import GeneralSettings from "./GerneralSettings";

function SettingsMenu() {
  const [activeButton, setActiveButton] = useState(true);
  const { handleButtonClick } = useContext(AppContext);
  const innerContainerRef = useRef(null);

  

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        innerContainerRef.current &&
        !innerContainerRef.current.contains(event.target)
      ) {
        handleButtonClick(); // Trigger the handleButtonClick function
      }
    };

    // Add event listener to detect clicks outside of the inner container
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [handleButtonClick]); // Include handleButtonClick in the dependency array

  const changeSettingMenu = (buttonName) => {
    setActiveButton(buttonName);
  };

  return (
    <Container fluid className="position-absolute top-0 settings-container">
      <Container ref={innerContainerRef} className="settings-window">
        <p className="mt-4 pb-3 border-bottom border-black" style={{fontSize:'22px'}}>Inställningar</p>
        <ButtonGroup className="w-100">
          <Button
            onClick={() => changeSettingMenu(true)} // Wrap in an arrow function
            className={`bg-${activeButton ? '2' : '1'} border-0 text-black general-button border-end`}
          >
            Allmänt
          </Button>
          <Button
            onClick={() => changeSettingMenu(false)} // Wrap in an arrow function
            className={`bg-${activeButton ? '1' : '2'} border-0 text-black data-button border-start`}
          >
            Data
          </Button>
        </ButtonGroup>
        {activeButton && <GeneralSettings />}
      </Container>
    </Container>
  );
}

export default SettingsMenu;
