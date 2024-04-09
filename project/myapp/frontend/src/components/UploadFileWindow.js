import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosDocument } from "react-icons/io";
import { IoIosCopy } from "react-icons/io";
import { AuthContext } from "./AuthContextProvider";
import FileDropZone from "./FileDropZone";

import { useContext } from "react";

function UploadFileWindow() {
  const { userID } = useContext(AuthContext);
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    // Check if the selected file is a PDF
    if (file.type !== "application/pdf") {
      alert("Please select a PDF file.");
      return;
    }
    console.log('userID:', userID)
    const body = { 
      file: file,
      userID: userID };
    console.log(body)
    headers = {
      'Content-Type': 'multipart/form-data',
    }
    try {

        const response = await fetch('http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/upload/', {
            method: 'POST',
            headers: headers,
            body: body
        });
        const data = await response.json();
        alert(`File uploaded successfully. Document ID: ${data.document_id}`);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  return (
    <Container className="m-auto p-2 h-75 bg-2 uploadfile-container">
      <Row className="h-10 w-100 bg-2 m-0 align-items-center d-flex justify-content-center">
        <h4 className="m-0">Upload document to start!</h4>
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
