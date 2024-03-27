
import { Col, Container, Row, Stack } from "react-bootstrap";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";

function SideMenuFiles() {
  const files = [
    {
      id: 1,
      name: "File 1",
    },
    {
      id: 2,
      name: "File 2",
    },
    {
      id: 3,
      name: "File 3",
    },
    {
      id: 1,
      name: "File 1",
    },
    {
      id: 2,
      name: "File 2",
    },
    {
      id: 3,
      name: "File 3",
    },
    {
      id: 1,
      name: "File 1",
    },
    {
      id: 2,
      name: "File 2",
    },
    {
      id: 3,
      name: "File 3",
    },
    {
      id: 1,
      name: "File 1",
    },
    {
      id: 2,
      name: "File 2",
    },
    {
      id: 3,
      name: "File 3",
    },
    {
      id: 1,
      name: "File 1",
    },
    {
      id: 2,
      name: "File 2",
    },
    {
      id: 3,
      name: "File 3",
    },
  ];
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