import { FaUser } from "react-icons/fa";
import Container from 'react-bootstrap/Container'
import Button from 'react-bootstrap/Button'
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { useState } from "react";
import { IoIosSettings } from "react-icons/io";
import { IoIosLogOut } from "react-icons/io";
function SideMenuBottom() {

    const [isVisible , setIsVisible] = useState(false);
    const toggleVisibility = () => {
        setIsVisible(!isVisible);
    };
    return (
        <Container className='position-relative'>
            <Container className=" position-absolute bottom-0 start-50 translate-middle-x mb-3">
           {isVisible && <Container>
                <ButtonGroup vertical className="w-100 bg-3 button-group-user">
                    <Button className="settings-button "><IoIosSettings size={25} className="settings-icon" />Settings</Button>
                    <Button className="logout-button"><IoIosLogOut size={25} className="logout-icon" />Log Out</Button>
                </ButtonGroup>
            </Container>}
            <Button className='bg-1 border-0 text-black person-button' onClick={toggleVisibility}> <FaUser className="user-icon"/> Julius Amorm</Button>
            </Container>
        </Container>    
    );
}

export default SideMenuBottom;