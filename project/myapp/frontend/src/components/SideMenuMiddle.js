import { Container, Button, Row } from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import axios from "axios";
import { FaTrashAlt } from "react-icons/fa";

function SideMenuMiddle({ clickedDocument, setClickedDocument }) {
  const { user } = useContext(AuthContext);
<<<<<<< Updated upstream
  const [showTimeline, setShowTimeline] = useState(false);
  const { files } = useContext(AuthContext);
  const { getFiles } = useContext(AuthContext);
  const {currentFile, setCurrentFile} = useContext(AuthContext);
  const {messages, setMessages} = useContext(ResponseContext);
=======
  const { files, currentFile, setCurrentFile } = useContext(AuthContext);
  const { messages, setMessages } = useContext(ResponseContext);
>>>>>>> Stashed changes
  const baseURL = process.env.REACT_APP_API_URL;

  

  const getChatHistory = async (fileid) => {
    const body = {
      embedding_id: fileid ? fileid : currentFile
    };
    try {
      const { data } = await axios.post(baseURL + "api/getchat/", body);
      setMessages(data.messages);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
    }
  };

  const deleteDocument = async (fileid) => {
<<<<<<< Updated upstream
    console.log('fileid:', fileid);
    const resp = await axios.post(baseURL+'api/deletefile/', {fileid: fileid, user: user.id});
=======
    const resp = await axios.post(baseURL + "api/deletefile/", { fileid: fileid });
>>>>>>> Stashed changes
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
        <div>
          asdasdasdasd
        </div>
      ) : (
        <>
          

<<<<<<< Updated upstream
      {showTimeline && <TimeLine />}
      <PerfectScrollbar>
      {files.map((file) => (
        <Row className=" my-4 overflow-scroll m-auto rounded-2 w-100 bg-3">
          <Button value={file.id} onClick={e => chooseDocument(e.target.value)} className="my-2 text-start"><IoIosDocument  size={30} /> { file.filename }</Button>
          <Button value={file.id} onClick={e => deleteDocument(e.target.value)}><FaTrashAlt /></Button>
        </Row>
        ), [files])}
        </PerfectScrollbar>
=======
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
>>>>>>> Stashed changes
    </Container>
  );
}

export default SideMenuMiddle;
