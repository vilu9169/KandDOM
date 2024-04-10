
import { Col, Container, Row, Stack } from "react-bootstrap";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { useState } from "react";

function SideMenuFiles() {
  const [files, setFiles] = useState([]);
  const getFiles = async (e) => {
    try {
      const response = await fetch("http://localhost:8000/api/documents/");
      const data = await response.json();
      console.log(data);
      return data;
    }
    catch (error) {
      console.error("Error fetching files:", error);
    }
  };
  getFiles()
  return (
    <Container className="h-100 file-window">
      <h3 className=" mt-3 ms-3 text-start">Filer</h3>

      <Col  className="h-100 files-scroll">
        <PerfectScrollbar>
      {files.map((file) => (
        <Row className=" my-4 m-auto rounded-2 w-100 bg-3">
          <p className="my-2 text-start"><IoIosDocument  size={30} /> {file.name}</p>
        </Row>
        ))}
        </PerfectScrollbar>
      </Col>

    </Container>
  );
}

export default SideMenuFiles;