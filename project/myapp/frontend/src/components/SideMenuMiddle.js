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
  const { timeLine, setTimeline, getTimeLine } = useContext(AuthContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const { pinRef } = useContext(ResponseContext);
  const { docGroups } = useContext(AuthContext);
  const { currentGroup, setCurrentGroup } = useContext(AuthContext);
  const { docsInGroup, setDocsInGroup } = useState([]);

  const getDocsInGroup = async () => {
    const body = {
      group: currentGroup,
    };
    console.log(body)
    try {
      const { data } = await axios.post(baseURL + "api/getdocsingroup/", body);
      console.log(data);
      setDocsInGroup(data.resp);
      return data;
    } catch (error) {
      console.error("Error getting documents in group:", error);
    }
  };
  
  const chooseDocument = (fileid) => {
    setCurrentFile(fileid);
    setCurrentGroup(null);
    localStorage.setItem("currentFile", fileid);
    localStorage.setItem("currentGroup", null);
    getChatHistory(fileid);
    getTimeLine(fileid);
    setClickedDocument(true);
  };
  const chooseGroup = (groupid) => {
    setCurrentFile(null);
    setCurrentGroup(groupid);
    localStorage.setItem("currentFile", null);
    localStorage.setItem("currentGroup", groupid);
    getChatHistory(groupid);
    getDocsInGroup();
    setClickedDocument(true);
  };


  return (
    <Container className="p-0">
      {clickedDocument ? (
        <>
          {pinnedMessages.map((pin) => (
            <Row key={pin.index} className="my-4 m-auto br-5 w-100">
              <Button
                className="m-auto bg-3 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start"
                onClick={() => {console.log(pin.index); return scrollToPin(pinRef , pin.index)}}
              >
                {pin.id}
              </Button>
            </Row>
          ))}
          {currentGroup && (
            <Row className="my-4 m-auto br-5 w-100">
              {docsInGroup.map((doc) => (
                // Code for rendering each document in the group
                <div>{doc.filename}</div> // Replace with appropriate rendering logic
              ))}
            </Row>
          )}
        </>
      ) : (
        <>
          <hr className="w-90 m-auto" />
          <PerfectScrollbar>
            Document Groups
            {docGroups.map((docGroup) => (
              <Row key={docGroup.id} className="my-3 m-auto br-5 w-100">
              <Button
                onClick={() => chooseGroup(docGroup.id)}
                value={docGroup.id}
                className={`small m-auto bg-2 w-90 document-button d-flex justify-content-start align-items-center p-2 text-start position-relative ${
                  docGroup.id === currentGroup ? "highlighted" : ""
                }`}
              >
                {docGroup.name}
                <Container
                  className={`p-1 w-80px h-100 d-flex justify-content-center align-items-center ${
                    docGroup.id === currentGroup
                      ? "highlighted-iconbox"
                      : "icons-container"
                  }`}
                >
                  <SimplePopup file={docGroup} 
                  />
                  <IoIosArchive
                    className="m-2 archive-icon"
                    onClick={() => console.log("Edit document")}
                  />
                </Container>
              </Button>
            </Row>
            ))
            }
            Documents
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
                    <SimplePopup file={file} 
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
