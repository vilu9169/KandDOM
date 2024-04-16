import { Container, Button } from "react-bootstrap";
import { useContext, useState } from "react";
import TimeLine from "./TimeLine";
import { TbTimelineEventFilled } from "react-icons/tb";
import PerfectScrollbar from "react-perfect-scrollbar";
import { IoIosDocument } from "react-icons/io";
import { Row } from "react-bootstrap";
import { AuthContext } from "./AuthContextProvider";

function SideMenuMiddle() {
  const [showTimeline, setShowTimeline] = useState(false);
  const { files } = useContext(AuthContext);
  const handleButtonClick = () => {
    setShowTimeline(!showTimeline);
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
        <Row className=" my-4 m-auto rounded-2 w-100 bg-3">
          <p className="my-2 text-start"><IoIosDocument  size={30} /> { file.filename } </p>
        </Row>
        ), [files])}
        </PerfectScrollbar>
    </Container>
  );
}

export default SideMenuMiddle;
