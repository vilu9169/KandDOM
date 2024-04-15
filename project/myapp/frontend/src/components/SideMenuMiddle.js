import { Container, Button, ButtonGroup } from "react-bootstrap";
import { AppContext } from "./ShowSettingsHandler";
import { useContext, useEffect, useRef, useState } from "react";
import TimeLine from "./TimeLine";
import { TbTimelineEventFilled } from "react-icons/tb";
import { AuthContext } from "./AuthContextProvider";

function SideMenuMiddle() {
  const { user } = useContext(AuthContext);
  const [showTimeline, setShowTimeline] = useState(false);
  
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
    </Container>
  );
}

export default SideMenuMiddle;
