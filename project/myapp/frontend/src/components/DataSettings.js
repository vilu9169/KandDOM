import { Button, Container, Row, Col, Form } from "react-bootstrap";
import { AuthContext } from "./AuthContextProvider";
import React, { useContext, useState, useEffect } from "react";

import { alpha, styled } from "@mui/material/styles";
import Switch from "@mui/material/Switch";

const OurSwitch = styled(Switch)(({ theme }) => ({
  "& .MuiSwitch-switchBase.Mui-checked": {
    color: "#0f2c59",
    "&:hover": {
      backgroundColor: alpha("#0f2c59", theme.palette.action.hoverOpacity),
    },
  },
  "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
    backgroundColor: "#0f2c59",
  },
}));

function DataSettings() {
  const { user } = useContext(AuthContext);
  const [userName] = useState(user.name);
  const [userEmail] = useState(user.email);

  const [deleteClicked, setDeleteClicked] = useState(false);

  const handleDeleteClick = () => {
    if (deleteClicked) {
      // Handle account deletion logic here
      // For now, let's just log a message
      console.log("Account deleted!");
    } else {
      // First click, set deleteClicked to true
      setDeleteClicked(true);
      // Reset deleteClicked after a certain time (e.g., 3 seconds) if second click doesn't occur
      setTimeout(() => {
        setDeleteClicked(false);
      }, 3000); // Adjust the time as needed
    }
  };

  return (
    <Container className="h-50">
      <Row className="p-3">
        <Col className="col-6 d-flex align-items-center">Name: </Col>
        <Col className="col-6 d-flex justify-content-center align-items-center">
          {userName}
        </Col>
      </Row>
      <hr className="w-90 m-auto" />
      <Row className="p-3 d-flex align-items-center">
        <Col className="col-6 d-flex align-items-center">Email:</Col>
        <Col className="col-6 d-flex justify-content-center align-items-center">
          {userEmail}
        </Col>
      </Row>
      <hr className="w-90 m-auto" />
      <Row className="p-3 d-flex align-items-center">
        <Col className="col-3 d-flex align-items-center">SekretesLäge</Col>
        <Col className="col-6 d-flex align-items-center">
          <span className="small-setting-text">
            När sekretessläget är aktiverat, lagrar vi inte dokumenten i vår
            databas. Observera att detta även innebär att dokumenten samt all
            konversation kring dem kommer att försvinna när du loggar ut.
          </span>
        </Col>
        <Col className="col-3 d-flex justify-content-center align-items-center">
          <OurSwitch size="small" />
        </Col>
      </Row>
      <hr className="w-90 m-auto" />
      <Row className="p-3 d-flex align-items-center">
        <Col className="col-9 d-flex align-items-center">Radera konto:</Col>
        <Col className="col-3 d-flex justify-content-center align-items-center">
          <Button className="btn-danger" onClick={handleDeleteClick}>
            {deleteClicked ? "Klicka igen" : "Ta bort"}
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default DataSettings;
