import { Container, Button, Row } from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import axios from "axios";

import { scrollToPin } from "./Chatbot";
import { IoIosArchive } from "react-icons/io";
import SimplePopup from "./ThreeDotLogic";

function SideMenuMiddle({ clickedDocument, setClickedDocument }) {
  const { user } = useContext(AuthContext);
  const { pinnedMessages } = useContext(ResponseContext);
  const [showTimeline, setShowTimeline] = useState(false);

  const { files, getFiles, currentFile, setCurrentFile } = useContext(AuthContext);
  const { messages, setMessages, getChatHistory } = useContext(ResponseContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const { pinRef } = useContext(ResponseContext);
  const deleteDocument = async (fileid) => {
    console.log('fileid:', fileid);
    const resp = await axios.post(baseURL + 'api/deletefile/', { fileid: fileid, user: user.id });
    console.log(resp);
    getFiles();
  };

  /*
  const deleteDocument = async (fileid) => {
    console.log("fileid:", fileid);
    const resp = await axios.post(baseURL + "api/deletefile/", {
      fileid: fileid,
      user: user.id,
    });
  */
  


  const chooseDocument = (fileid) => {
    setCurrentFile(fileid);
    localStorage.setItem("currentFile", fileid);
    getChatHistory(fileid);
    setClickedDocument(true);
  };

  return (
    <Container className="p-0">
      {clickedDocument ? (
        pinnedMessages.map((pin, index) => (
          <Row key={pin.id} className="my-4 m-auto br-5 w-100">
            <Button
              classname="m-auto bg-3 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start"
              
              onClick={() => scrollToPin(pinRef.current[index])}
              >
                {pin.filename}
                {pin}
              </Button>
          </Row>
        ))

      ) : (
        <>
          <hr className="w-90 m-auto" />
          <PerfectScrollbar>
            {files.map((file) => (
              <Row key={file.id} className="my-3 m-auto br-5 w-100">
                <Button
                  onClick={() => chooseDocument(file.id)}
                  value={file.id}
                  className={`small m-auto bg-2 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start position-relative ${
                    file.id === currentFile ? "highlighted" : ""
                  }`}
                >
                  {file.filename}
                  <Container
                    className={`p-1 w-80px h-100 d-flex justify-content-center align-items-center ${
                      file.id === currentFile
                        ? "highlighted-iconbox"
                        : "icons-container"
                    }`}
                  >
                    <SimplePopup
                      onDeleteClick={() => deleteDocument(file.id)}
                    />
                    <IoIosArchive
                      className="m-2 archive-icon"
                      onClick={() => console.log("Edit document")}
                    />
                  </Container>
                </Button>
              </Row>
            ))}
          </PerfectScrollbar>
        </>
      )}
    </Container>
  );
}

export default SideMenuMiddle;
