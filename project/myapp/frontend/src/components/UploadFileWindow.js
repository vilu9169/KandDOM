import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosDocument } from "react-icons/io";
import { IoIosCopy } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import FileDropZone from "./FileDropZone";
import { useContext, useEffect, useState } from "react";
import { UploadWindowContext } from "./UploadWindowContextProvider";

function UploadFileWindow() {
  const { value } = useContext(UploadWindowContext);
  const { userID, getFiles } = useContext(AuthContext);
  const { setCurrentFile } = useContext(AuthContext);
  const [title, setTitle] = useState("Upload document to start!");

  const baseURL = process.env.REACT_APP_API_URL;
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    // Check if the selected file is a PDF
    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }
    console.log('userID:', userID)
    let formData = new FormData();

    formData.append('file', file); // Append the file to FormData
    formData.append('userID', userID);
    console.log(baseURL+'upload/')
    try {
        const response = await fetch(baseURL+'upload/', {

            method: 'POST',
            body: formData
        });
        const data = await response.json();
        getFiles()
        setCurrentFile(data.document_id)
        localStorage.setItem('currentFile', data.document_id)
        alert(`File uploaded successfully. Document ID: ${data.document_id}`);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
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

  return (
    <Container className="m-auto p-2 h-75 bg-2 uploadfile-container">
      <Row className="h-10 w-100 bg-2 m-0 align-items-center d-flex justify-content-center">
        <h4 className="m-0">{title}</h4>
      </Row>
      <Row className="p-0 h-90 w-100 bg-2  m-0">
        <Col className="col-5 p-0 bg-2 d-flex align-items-center justify-content-center">
          <FileDropZone></FileDropZone>
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
  );
}
export default UploadFileWindow;
