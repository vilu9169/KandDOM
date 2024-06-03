
import { Col, Container, Row, Stack } from "react-bootstrap";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { useEffect, useState } from "react";
import { useContext } from "react";
import { AuthContext } from "./AuthContextProvider";
import axios from "axios";

function SideMenuFiles() {
  const { files } = useContext(AuthContext);
  return (
    <Container className="h-100 file-window overflow-hidden">
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