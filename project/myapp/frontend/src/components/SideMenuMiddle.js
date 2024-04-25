import { Container, Button, Row } from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import axios from "axios";
import { FaTrashAlt } from "react-icons/fa";
import { scrollToPin } from "./Chatbot";

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


  const chooseDocument = (fileid) => {
    setCurrentFile(fileid);
    localStorage.setItem('currentFile', fileid);
    getChatHistory(fileid);
    setClickedDocument(true); // Set clickedDocument to true when a document is chosen
  };

  return (
    <Container className="p-0 mt-3">
      {clickedDocument ? (
        pinnedMessages.map((pin, index) => (
          <Row key={pin.id} className="my-4 m-auto br-5 w-100">
            <Button
              classname="m-auto bg-3 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start"
              
              onClick={() => scrollToPin(pinRef[index])}
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
              <Row key={file.id} className="my-4 m-auto br-5 w-100">
                <Button
                  onClick={() => chooseDocument(file.id)}
                  value={file.id}
                  className="m-auto bg-3 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start"
                >
                  {file.filename}
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
