import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { IoIosDocument } from "react-icons/io";
import { IoIosCopy } from "react-icons/io";
import axios from 'axios';
import React from 'react';


function UploadFileWindow() {

  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Retrieve CSRF token from cookie
      const csrftoken = getCookie('csrftoken');

      // Send POST request with CSRF token included in headers
      const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrftoken
        }
      });

      // Display success message with uploaded file name
      alert(`Uploaded file: ${file.name}`);
    } catch (error) {
      // Display error message if upload fails
      alert('Error uploading file');
      console.error(error);
    }
  };

  // Function to retrieve CSRF token from cookie
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  };

  return (
    <Container className="m-auto p-2 h-75 bg-2 uploadfile-container">
      <Row className="h-10 w-100 bg-2 m-0 align-items-center d-flex justify-content-center">
        <h4 className="m-0">Upload document to start!</h4>
      </Row>
      <Row className="p-0 h-90 w-100 bg-2  m-0">
        <Col className="col-5 p-0 bg-2">lol</Col>
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
