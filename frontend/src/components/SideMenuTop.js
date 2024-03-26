import { Button, Container } from "react-bootstrap";
import { IoIosDocument } from "react-icons/io";


function SideMenuTop() {

    return (
        <Container className="p-0 w-100 h-100 justify-content-center d-flex align-items-center">
            <Button className="m-auto bg-3 w-90 wide-button d-flex justify-content-center align-items-center p-1">
              <span className="text-center justify-content-center d-flex align-items-center w-75">Add document</span>
              <span className="w-25 justify-content-center d-flex align-items-center"><IoIosDocument className="size-20" /></span>
            </Button>
        </Container>
    );
}

export default SideMenuTop;