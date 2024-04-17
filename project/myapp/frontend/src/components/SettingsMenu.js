import { Container, Button, ButtonGroup, Row } from "react-bootstrap";
import { AppContext } from "./ShowSettingsHandler";
import { useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "./AuthContextProvider";
import GeneralSettings from "./GerneralSettings";
import DataSettings from "./DataSettings";

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
      <Container
        ref={innerContainerRef}
        className="bg-2 w-50 h-80 d-flex flex-column settings-window"
      >
        <Row className="h-60px d-flex justify-content-center align-items-center">
          <span style={{ fontSize: "22px" }}>Inställningar</span>
        </Row>
        <hr className="w-90 m-auto pb-2 " />
        <Row className="h-40px ">
          <ButtonGroup className="w-100">
            <Button
              onClick={() => changeSettingMenu(true)}
              className={`bg-${
                activeButton ? "1" : "2"
              } border-0 text-black general-button border-end`}
            >
              <p className="p-0 m-0">Allmänt</p>
            </Button>
            <Button
              onClick={() => changeSettingMenu(false)}
              className={`bg-${
                activeButton ? "2" : "1"
              } border-0 text-black data-button border-start`}
            >
              <p className="p-0 m-0">Data</p>
            </Button>
          </ButtonGroup>
        </Row>
        <Row className="flex-grow-1 br-5">{activeButton ? <GeneralSettings /> : <DataSettings />}</Row>
      </Container>
    </Container>
  );
}

export default SettingsMenu;
