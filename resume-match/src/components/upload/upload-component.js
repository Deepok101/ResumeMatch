import React, {useState} from "react";
import './upload-component.css'


import { Button, Snackbar } from "@material-ui/core"

function Upload() {

    const [uploadedFile, setUploadedFile] = useState(); 

    const uploadFile = async () =>{
        const formData = new FormData();

		formData.append('file', uploadedFile);

		const response = await fetch(
			'http://127.0.0.1:5000/api/upload',
			{
				method: 'POST',
				body: formData,
			}
		)

        const data = await response.json();
        console.log("this is data",data)
	
    }

    const setFile = (event) =>{
        setUploadedFile(event.target.files[0])
    }

    return(
        <div className="searchForm">
            {uploadedFile ?
            <div>
                A file has been uploaded
            </div> : <></>}
                <label htmlFor="fileUpload" className="fileUploadLabel">
                    Drag and drop to upload your Resume
                </label>
                <input onChange={setFile} type="file" id="fileUpload"/>
                <Button onClick={uploadFile} variant="contained" color="primary">
                    Search Button
                </Button>
            </div>
    )
}
export default Upload