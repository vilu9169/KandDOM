import React, { useEffect, useContext } from "react";
import { Unstable_Popup as BasePopup } from "@mui/base/Unstable_Popup";
import { BsThreeDots } from "react-icons/bs";
import { IoMdCreate } from "react-icons/io";
import { Container, Button } from "react-bootstrap";
import { IoMdTrash } from "react-icons/io";
import axios from "axios";
import { AuthContext } from "./AuthContextProvider";


export default function SimplePopup({ file }) {
  const [anchor, setAnchor] = React.useState(null);
  const { user, getFiles } = useContext(AuthContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const handleClick = (event) => {
    event.stopPropagation(); // Stop propagation to prevent document-button click
    setAnchor(anchor ? null : event.currentTarget);
  };
  const deleteDocument = async (fileid) => {
    console.log('fileid:', fileid);
    const resp = await axios.post(baseURL + 'api/deletefile/', { fileid: fileid, user: user.id });
    console.log(resp);
    getFiles();
  };
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (anchor && !anchor.contains(event.target)) {
        setAnchor(null);
      }
    };

    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [anchor]);

  const open = Boolean(anchor);
  const id = open ? "simple-popper" : undefined;


  return (
    <div className="m-2">
      <button
        className="p-0 iconButton d-flex justify-content-start align-items-center"
        aria-describedby={id}
        type="button"
        onClick={handleClick}
      >
        <BsThreeDots />
      </button>
      <BasePopup id={id} open={open} anchor={anchor}>
        <div className="p-2 popupBody">
          <Button
            className="m-auto my-2 bg-3 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
          >
            <span className="small text-center justify-content-center d-flex align-items-center w-75">
              Rename Chat
            </span>
            <span className="w-25 justify-content-center d-flex align-items-center">
              <IoMdCreate className="size-20" />
            </span>
          </Button>
          <Button
            className="m-auto my-2 bg-danger w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
          >
            <span className="small text-center justify-content-center d-flex align-items-center w-75">
              Delete Chat
            </span>
            <span className="w-25 justify-content-center d-flex align-items-center">
              <IoMdTrash className="size-20" onDeleteClick={() => deleteDocument(file.id)}/>
            </span>
          </Button>
        </div>
      </BasePopup>
    </div>
  );
}
