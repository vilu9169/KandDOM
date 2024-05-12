import React, { useEffect, useContext, useState } from "react";
import { Unstable_Popup as BasePopup } from "@mui/base/Unstable_Popup";
import { BsThreeDots } from "react-icons/bs";
import { IoMdCreate } from "react-icons/io";
import { Container, Button } from "react-bootstrap";
import { IoMdTrash } from "react-icons/io";
import axios from "axios";
import { AuthContext } from "./AuthContextProvider";
import { MdOutlineOpenInNew } from "react-icons/md";


export default function SimplePopup({ file, is_group }) {
  const [anchor, setAnchor] = React.useState(null);
  const [editing, setEditing] = useState(false);
  const [newName, setNewName] = useState("");
  const { user, getFiles } = useContext(AuthContext);
  const baseURL = process.env.REACT_APP_API_URL;
  const handleClick = (event) => {
    event.stopPropagation();
    setAnchor(anchor ? null : event.currentTarget);
  };
  const deleteDocument = async (fileid, event) => {
    console.log('fileid:', fileid);
    const resp = await axios.post(baseURL + 'api/deletefile/', { fileid: fileid, user: user.id });
    console.log(resp);
    getFiles();
  };
  const deleteGroup = async (fileid, event) => {
    console.log('fileid:', fileid);
    const resp = await axios.post(baseURL + 'api/deleteDocGroup/', { fileid: fileid, user: user.id });
    console.log(resp);
    getFiles();
  };

  const handleDelete = async (event) => {
    if (is_group) {
      deleteGroup(file.id);
    }
    else {
      deleteDocument(file.id);
    }
  };
  const handleRename = async () => {
    if (!editing) {
      setEditing(true);
    } else {
      try {
        const resp = await axios.post(baseURL + 'api/renamefile/', {
          fileid: file.id,
          user: user.id,
          new_name: newName,
        });
        console.log(resp);
        getFiles();
        setEditing(false);
      } catch (error) {
        console.error("Error renaming chat:", error);
      }
    }
  };
  const handleInputKeyDown = async (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      await handleRename();
      setEditing(false);
    }
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


  const openPdf = async (fileid, page) => {
    try {
      console.log('fileid:', fileid);
      console.log('page', page);
      
      const resp = await axios.post(baseURL + 'api/openpdf/', { fileid: fileid, page: page }, { responseType: 'blob' });

      // Check if the response contains the PDF file
      if (resp.status === 200 && resp.data) {
        // Create a Blob object from the response data
        const blob = new Blob([resp.data], { type: 'application/pdf' });
        
        // Create a URL for the Blob object 
        const url = URL.createObjectURL(blob);

        const pageURL = page ? `${url}#page=${page}` : url;
        
        // Open the PDF file in a new window or tab
        window.open(pageURL, '_blank');
      } else {
        // Handle the case where the PDF file is not found or response is empty
        console.error('Failed to open PDF: File not found or response is empty');
      }
    }catch (error) {
      // Handle any errors that occur during the request
      console.error('Error opening PDF:', error);
    }
  };

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
        {editing ? (
            <input
            type="text"
            className="m-auto my-2 bg-1 w-90 rename-input d-flex justify-content-center align-items-center p-0"
            placeholder="Enter new name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={handleInputKeyDown}
            onClick={(event) => {
              event.stopPropagation();
            }}
          />
          ) : (
            <Button
            onClick={(event) => {
              event.stopPropagation(); 
              handleRename();
            }}
              className="m-auto my-2 bg-3s w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
            >
              <span className="small text-center justify-content-center d-flex align-items-center w-75">
                Rename Chat
              </span>
              <span className="w-25 justify-content-center d-flex align-items-center">
                <IoMdCreate className="size-20" />
              </span>
            </Button>
          )}
          <Button
            className="m-auto my-2 w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
            onClick={() => openPdf(file.id, 0)}
            value={file.id}
          >
            <span className="small text-center justify-content-center d-flex align-items-center w-75">
              View PDF
            </span>
            <span className="w-25 justify-content-center d-flex align-items-center">
              <MdOutlineOpenInNew className="size-20" />
            </span>
          </Button>
          <Button
            onClick={(event) => {
              event.stopPropagation();
              deleteDocument(file.id);
            }}
            className="m-auto my-2 bg-danger w-90 pop-up-button d-flex justify-content-center align-items-center p-1"
          >
            <span className="small text-center justify-content-center d-flex align-items-center w-75">
              Delete Chat
            </span>
            <span className="w-25 justify-content-center d-flex align-items-center">
              <IoMdTrash className="size-20" />
            </span>
          </Button>
        </div>
      </BasePopup>
    </div>
  );
}
