import { Button, Container } from "react-bootstrap";



function SideMenuTop() {

    return (
        <Container className=" w-75 h-10 border-black border-bottom">
            <Button className="top-menu-button">
                Ladda upp dokument
            </Button>
        </Container>
    );
}

export default SideMenuTop;