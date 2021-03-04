import React, { useState } from "react"
import "./upload-component.css"

import { Button, TextField } from "@material-ui/core"

function Upload() {
    const [uploadedFile, setUploadedFile] = useState()
    const [searchQuery, setSearchQuery] = useState({
        'job':'',
        'location':''
    })

    const updateFormFields = (event, key) =>{
        setSearchQuery({...searchQuery, [key]: event.target.value})
    }

    const uploadFile = async () => {
        const formData = new FormData()

        formData.append("file", uploadedFile)

        const response = await fetch("http://127.0.0.1:5000/api/upload", {
            method: "POST",
            body: formData,
        })

        const data = await response.json()
        console.log("this is data", data)
    }

    const setFile = (event) => {
        setUploadedFile(event.target.files[0])
        console.log(event.target.files[0])
    }

    return (
        <div className="search-section">
            <form className="searchForm" noValidate autoComplete="off">
                <TextField 
                    onChange={(event) => updateFormFields (event, 'job')}
                    value={searchQuery['job']} 
                    className="textBox" 
                    id="job" 
                    label="Job" 
                />
                <TextField
                    onChange={(event) => updateFormFields (event, 'location')}
                    value={searchQuery['location']}
                    className="textBox"
                    id="location"
                    label="Location"
                />
            </form> 

            <div className="searchForm" >
                <label htmlFor="fileUpload" className="fileUploadLabel">
                    {uploadedFile ? (
                        <div>Uploaded File: {uploadedFile.name}</div>
                    ) : (
                        <div>Drag and drop to upload your Resume</div>
                    )}
                </label>
                <input onChange={setFile} type="file" id="fileUpload" />
                <Button onClick={uploadFile} variant="contained" color="primary">
                    Search Button
                </Button>
            </div>
        </div>
    )
}
export default Upload
