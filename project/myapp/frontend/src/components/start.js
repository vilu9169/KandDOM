import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import MyForm from "./Form";
import UploadFileWindow from "./UploadFileWindow";
import { IoMdHelp } from "react-icons/io";
import SideMenuBottom from "./SideMenuBottom";
import SettingsMenu from "./SettingsMenu";
import { showInfoWindowContext } from "./ShowInfoWindowContextProvider.js";
import { useContext, useState } from "react";
import { AppContext } from "./ShowSettingsHandler";
import SideMenuTop from "./SideMenuTop";
import SideMenuMiddle from "./SideMenuMiddle";
import Chatbot from "./Chatbot.js";
import InfoWindow from "./InfoWindow.js";
import { AuthContext } from "./AuthContextProvider";
import { UploadWindowContext } from "./UploadWindowContextProvider";
import apolloLogo from "../assets/apollo.png";

function Start() {
  const { buttonClicked } = useContext(AppContext);
  const { showInfoWindow, handleShowInfo } = useContext(showInfoWindowContext);
  const { user } = useContext(AuthContext);
  const { showUploadWindow } = useContext(UploadWindowContext);

  const [clickedDocument, setClickedDocument] = useState(false); // Changed initial value to false

  const handleDocumentButtonClick = (fileId) => {
    // Set clickedDocument state to true when a document button is clicked
    setClickedDocument(true);
    console.log("Clicked document with id:", fileId);
  };
  return (
    <>
      <Container fluid className="position-absolute h-100 text-center bg-3">
        <Row className="h-100">
          <Col color="" className="col main-left d-flex flex-column">
            <Row className="h-60px bg-2">
              <SideMenuTop clickedDocument={clickedDocument} />
            </Row>
            <Row className="flex-grow-1 bg-2">
              <SideMenuMiddle
                clickedDocument={clickedDocument}
                setClickedDocument={setClickedDocument}
              />
            </Row>
            <Row className="h-80px  bg-2">
              <SideMenuBottom clickedDocument={clickedDocument} />
            </Row>
          </Col>
          <Col className="col d-flex flex-column main-right">
            <Row className="h-60px bg-3">
              <Row className="h-100 bg-1 m-auto">
                <Col className="col-6 h-100 bg-1 align-items-end d-flex justify-content-start">
                  <h2 className="p-0 m-0">Pythia</h2>
                  <img
                    className="p-0 m-0 main-logo"
                    src={apolloLogo}
                    alt="apolloLogo"
                  />
                </Col>
                <Col className=" col-6 h-100 d-flex align-items-end justify-content-end">
                  <Button
                    onClick={handleShowInfo}
                    className="bg-3 rect-button align-items-center d-flex justify-content-center p-0"
                  >
                    <IoMdHelp className="size-20" />
                  </Button>
                </Col>
              </Row>
            </Row>
            <Row className=" flex-grow-1 bg-1 position-relative">
              {showUploadWindow && <UploadFileWindow />}
              <Chatbot></Chatbot>
            </Row>
            <Row className="h-80px bg-1 align-items-top">
              <MyForm></MyForm>
            </Row>
          </Col>
        </Row>
      </Container>
      {buttonClicked && <SettingsMenu />}
      {showInfoWindow && <InfoWindow />}
    </>
  );
}

export default Start;
