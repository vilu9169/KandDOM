
import file_icon from '../img/file_icon.png'
import person_icon from '../img/person_icon.png'
function SideMenu() {
    return (
    <div>
        <div className=' h-100 position-absolute' style={{width:'40vh',backgroundColor:'var(--main-color)'}}>
            <a href=''>
            <div className="doc-upload-button">
                <img src={file_icon} style={{height:'35px'}} />
                UPLOAD DOCUMENT
            </div>
            </a>
            <div className='profile-button'>
            <img src={person_icon} style={{height:'35px'}} />
            Julio Amorm
            </div>
        </div>
    </div>
    );
}

export default SideMenu;