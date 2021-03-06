import React, { useState } from "react"
import "./upload-component.css"

import { Button, TextField } from "@material-ui/core"

function Upload({ setJobPostings }) {
    const [uploadedFile, setUploadedFile] = useState()
    const [searchQuery, setSearchQuery] = useState({
        job: "",
        location: "",
    })

    const updateFormFields = (event, key) => {
        setSearchQuery({ ...searchQuery, [key]: event.target.value })
    }

    const uploadFile = async () => {
        const formData = new FormData()

        const blob = new Blob([JSON.stringify(searchQuery)],{
            type: 'application/json'
        })

        formData.append("file", uploadedFile)
        formData.append("query", blob)

        const response = await fetch("http://127.0.0.1:5000/api/upload", {
            method: "POST",
            body: formData,
        })

        const status = await response.status
        console.log(status)
        const data = await response.json()

        if (status === 200) {
            setJobPostings(
                data['data']
            )
        }
    }

    const setFile = (event) => {
        setUploadedFile(event.target.files[0])
        console.log(event.target.files[0])
    }

    return (
        <div className="search-section">
            <form encType="multipart/form-data" className="searchForm" noValidate autoComplete="off">
                <TextField
                    onChange={(event) => updateFormFields(event, "job")}
                    value={searchQuery["job"]}
                    className="textBox"
                    id="job"
                    label="Job"
                />
                <TextField
                    onChange={(event) => updateFormFields(event, "location")}
                    value={searchQuery["location"]}
                    className="textBox"
                    id="location"
                    label="Location"
                />
                <div className="searchForm">
                    <label htmlFor="fileUpload" className="fileUploadLabel">
                        {uploadedFile ? (
                            <div>Uploaded File: {uploadedFile.name}</div>
                        ) : (
                            <div>Drag and drop to upload your Resume</div>
                        )}
                    </label>
                    <input onChange={setFile} type="file" id="fileUpload" />
                    <Button
                        className="searchButton"
                        onClick={uploadFile}
                        variant="contained"
                        color="primary"
                    >
                        Search
                    </Button>
                </div>
            </form>
        </div>
    )
}
export default Upload
