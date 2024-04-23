import { Container, Button } from "react-bootstrap";
import { useContext, useEffect, useState } from "react";
import TimeLine from "./TimeLine";
import { TbTimelineEventFilled } from "react-icons/tb";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { Row } from "react-bootstrap";
import { AuthContext } from "./AuthContextProvider";
import { ResponseContext } from "./ResponseContextProvider";
import axios from "axios";

function SideMenuMiddle() {
  const [showTimeline, setShowTimeline] = useState(false);
  const { files } = useContext(AuthContext);
  const {currentFile, setCurrentFile} = useContext(AuthContext);
  const {messages, setMessages} = useContext(ResponseContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const handleButtonClick = () => {
    setShowTimeline(!showTimeline);
  };
  const getChatHistory = async () => {
    const body = {
      embedding_id: currentFile
    }
    try {
      const {data} = await axios.post(baseURL+'api/getchat/', body);
      console.log(data);
      console.log(data.messages);
      setMessages(data.messages);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setMessages([]);
    }
  };
  const deleteDocument = async (fileid) => {
    const resp = await axios.post(baseURL+'api/deletefile/', {fileid: fileid});
    console.log(resp);
  };
  useEffect(() => console.log('currentFile:', currentFile), [currentFile]);
  const chooseDocument = async (fileid) => {
    console.log('file:', fileid);
    setCurrentFile(prevFile => {
      // Use the latest value of fileid
      const newFile = fileid;
      localStorage.setItem('currentFile', newFile);
      return newFile;
    });
    await getChatHistory();
  };
  return (
    <Container className="p-0 mt-3">
      <Button
          onClick={handleButtonClick}
          className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1"
        >
          <span className="text-center justify-content-center d-flex align-items-center w-75">
            Timeline
          </span>
          <span className="w-25 justify-content-center d-flex align-items-center">
            <TbTimelineEventFilled className="size-20" />
          </span>
        </Button>
      {showTimeline && <TimeLine />}
      <PerfectScrollbar>
      {files.map((file) => (
        <Row className=" my-4 overflow-scroll m-auto rounded-2 w-100 bg-3">
          <Button value={file.id} onClick={e => chooseDocument(e.target.value)} className="my-2 text-start"><IoIosDocument  size={30} /> { file.filename } </Button>
        </Row>
        ), [files])}
        </PerfectScrollbar>
    </Container>
  );
}

export default SideMenuMiddle;
