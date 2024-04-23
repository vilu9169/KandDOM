
import { Col, Container, Row, Stack } from "react-bootstrap";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { useState } from "react";
import { useContext } from "react";
import { AuthContext } from "./AuthContextProvider";
import axios from "axios";

function SideMenuFiles() {
  const { userID } = useContext(AuthContext);
  const [files, setFiles] = useState([]);

  const body = {
    "userID": userID,
  }
  // const getFiles = async (e) => {
  //   try {
  //     const response = await axios.post("http://ec2-16-171-79-116.eu-north-1.compute.amazonaws.com:8000/api/documents/", body);
  //     const data = await response.json();
  //     console.log(data);
  //     let fileArr = []
  //     for (const file in data) {
  //       console.log(file);
  //       fileArr.push(file.name);
  //     }
  //     setFiles(fileArr);
  //     return data;
  //   }
  //   catch (error) {
  //     console.error("Error fetching files:", error);
  //   }
  // };
  // getFiles()
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