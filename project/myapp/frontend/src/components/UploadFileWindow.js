import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosDocument } from "react-icons/io";
import { IoIosCopy } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import PerfectScrollbar from "react-perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import FileDropZone from "./FileDropZone";
import { useContext, useEffect, useState, useRef } from "react";
import { UploadWindowContext } from "./UploadWindowContextProvider";
import LoadingScreen  from "./LoadingScreen";
import axios from "axios";
function UploadFileWindow({clickedDocument, setClickedDocument}) {
  const { value } = useContext(UploadWindowContext);
  const { userID, getFiles } = useContext(AuthContext);
  const { currentFile, setCurrentFile } = useContext(AuthContext);
  const [title, setTitle] = useState("Upload document to start!");
  const { docGroups,  getDocumentGroups } = useContext(AuthContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const { currentGroup, setCurrentGroup } = useContext(AuthContext);
  const [ loading, setLoading ] = useState(false);
  const  [ loadingText, setLoadingText ] = useState("");
  const { files } = useContext(AuthContext);
  const createDocGroup = async (fileid) => {
    const body = {
      user: userID,
      new_doc: fileid,
      current: currentFile,
      name: "Group " + docGroups.length,
    };
    try {
      const { data } = await axios.post(baseURL + "api/createDocgroup/", body);
      console.log(data);
      getDocumentGroups();
      setCurrentGroup(data.docID);
      return data;
    } catch (error) {
      console.error("Error creating document group:", error);
    }
  }

  const updateDocgroup = async (fileid) => {
    const body = {
      user: userID,
      new_doc: fileid,
      docgroup: currentGroup,
    };
    try {
      const { data } = await axios.post(baseURL + "api/updateDocgroup/", body);
      console.log(data);
      getDocumentGroups();
      setCurrentGroup(data.docID);
      return data;
    } catch (error) {
      console.error("Error updating document group:", error);
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    // Check if the selected file is a PDF
    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }
    console.log('userID:', userID)
    let formData = new FormData();

    const group = !(currentGroup === null) ? 1 : 0;
    console.log('group:', group)
    formData.append('file', file); // Append the file to FormData
    formData.append('userID', userID);
    formData.append('group', group);
    console.log(baseURL+'upload/')
    try {
        setLoading(true);
        setLoadingText('Uploading file...')
        const response = await fetch(baseURL+'upload/', {

            method: 'POST',
            body: formData
        });
        const data = await response.json();
            console.log(`File uploaded successfully. Document ID: ${data.document_id}`);
            if (value === 2 && !currentGroup){
              setLoadingText('Creating new group...')
              createDocGroup(data.document_id)
                .then(() => {
                  setLoading(false);
                });
            }
            else if (value === 2 && currentGroup){
              setLoadingText('Updating group...')
              updateDocgroup(data.document_id)
                .then(() => {
                  setLoading(false);
                });
            }
            else {
              setLoadingText('')
              setLoading(false);
            }
            getFiles();
            getDocumentGroups();

    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
      setLoading(false)
    }
  };
  
  useEffect(() => {
    if (value === 1) {
      setTitle("Upload document to a new chat.");
    } else if (value === 2) {
      setTitle("Upload document to current existing chat.");
    } else {
      setTitle("Upload document to start!");
    }
  }, [value]);

  const chooseDocument = (fileid) => {
    setCurrentFile(fileid);
    setCurrentGroup(null);
    localStorage.setItem("currentFile", fileid);
    localStorage.setItem("currentGroup", null);
    setClickedDocument(true);
  };
  const chooseGroup = (groupid) => {
    setCurrentFile(null);
    setCurrentGroup(groupid);
    localStorage.setItem("currentFile", null);
    localStorage.setItem("currentGroup", groupid);
    setClickedDocument(true);
  };

  return (
    <>
    {loading ? (
      <LoadingScreen loadingText={loadingText}/>
    ) : (
    <Container className="m-auto p-2 h-75 bg-2 uploadfile-container">
      <Row className="h-10 w-100 bg-2 m-0 align-items-center d-flex justify-content-center">
        <h4 className="m-0">{title}</h4>
      </Row>
      <Row className="p-0 h-90 w-100 bg-2  m-0">
        <Col className="col-5 p-0 bg-2 d-flex align-items-center justify-content-center">
        <PerfectScrollbar className="scrollFiles2">
          <Container className="filesScroll2">
        {value === 2 ? (
          <>
            { (docGroups !== null) ? <>Document Groups</> : <></>}
            {docGroups.map((docGroup) => (
              <Row key={docGroup.id} className="my-3 m-auto br-5 w-100">
                <Button
                  onClick={() => chooseGroup(docGroup.id)}
                  value={docGroup.id}
                  className={`small m-auto bg-2 w-90 document-button2 d-flex justify-content-start align-items-center p-2 text-start position-relative ${
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
                  </Container>
                </Button>
              </Row>
            ))}
            Docuents:
            {files.map((file) => (
              <Row key={file.id} className="my-3 m-auto br-5 w-100">
                <Button
                  onClick={() => chooseDocument(file.id)}
                  value={file.id}
                  className={`small m-auto bg-2 w-90 document-button2 d-flex justify-content-start align-items-center p-2 text-start position-relative ${
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
                  </Container>
                </Button>
              </Row>
            ))}
          </>
        ) : (
          <FileDropZone />
        )}
        </Container>
        </PerfectScrollbar>

        </Col>
        <Col className="col-2 p-0 bg-2 d-flex align-items-center justify-content-center position-relative">
          <div className="vertical-line"></div>
          <div className="middle-box d-flex align-items-center justify-content-center">
            or
          </div>
        </Col>

        <Col className="col-5 p-0">
          <Row className="h-50 w-100 bg-2 m-0">
            <label
              htmlFor="file-upload"
              className="m-auto bg-3 w-75 wide-button d-flex justify-content-center align-items-center p-0"
            >
              <span className="text-center justify-content-center d-flex align-items-center w-75">
                Choose file
              </span>
              <span className="w-25 justify-content-center d-flex align-items-center">
                <IoIosDocument className="size-20" />
              </span>
            </label>
            <input
              id="file-upload"
              type="file"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
          </Row>
          <Row className="h-50 w-100 bg-2 m-0">
            <Button className="m-auto bg-3 w-75 wide-button d-flex justify-content-center align-items-center p-0">
              <span className="text-center justify-content-center d-flex align-items-center w-75">
                Copy text
              </span>
              <span className="w-25 justify-content-center d-flex align-items-center">
                <IoIosCopy className="size-20" />
              </span>
            </Button>
          </Row>
        </Col>
      </Row>
    </Container>
  )};
  </>
  );
}
export default UploadFileWindow;
