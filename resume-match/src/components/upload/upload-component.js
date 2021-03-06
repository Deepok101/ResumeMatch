import React, { useEffect, useState } from "react"
import "./upload-component.css"

import { Button, TextField, Snackbar } from "@material-ui/core"
import { Alert } from "@material-ui/lab"

function Upload({ setJobPostings }) {
    const [uploadedFile, setUploadedFile] = useState()
    const [searchQuery, setSearchQuery] = useState({
        job: "",
        location: "",
    })
    const [snackBarState, setSnackBarState] = useState({
        open: false,
        message: "",
        autoHideDuration: null,
        severity: "warning",
    })

    const [jobSpecialChar, setJobSpecialChar] = useState(false)
    const [locationSpecialChar, setLocationSpecialChar] = useState(false)

    const { open, message, autoHideDuration, severity } = snackBarState

    const onClose = () => {
        setSnackBarState({ ...snackBarState, open: false })
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
    const specialCharacters = new RegExp(/[!@#$%^&*()_+\-=[\]{};':"\\|<>/?]+/)

    useEffect(() => {
        if (specialCharacters.test(searchQuery.job)) {
            setJobSpecialChar(true)
        } else {
            setJobSpecialChar(false)
        }
        if (specialCharacters.test(searchQuery.location)) {
            setLocationSpecialChar(true)
        } else {
            setLocationSpecialChar(false)
        }
    }, [searchQuery, specialCharacters])

    const updateFormFields = (event, key) => {
        setSearchQuery({ ...searchQuery, [key]: event.target.value })

        console.log("")
    }

    const uploadFile = async () => {
        console.log(uploadedFile)
        if (!uploadedFile) {
            setSnackBarState({
                open: true,
                message: "Please submit a CV!",
                autoHideDuration: 2000,
                severity: "warning",
            })
        } else if (searchQuery.job.replace(/\s+/g, "") === "") {
            setSnackBarState({
                open: true,
                message: "Please input a job!",
                autoHideDuration: 2000,
                severity: "warning",
            })
        } else if (searchQuery.location.replace(/\s+/g, "") === "") {
            setSnackBarState({
                open: true,
                message: "Please input a location",
                autoHideDuration: 2000,
                severity: "warning",
            })
        } else if (specialCharacters.test(searchQuery.job)) {
            setSnackBarState({
                open: true,
                message: "Job contains special characters",
                autoHideDuration: 2000,
                severity: "warning",
            })
        } else if (specialCharacters.test(searchQuery.location)) {
            setSnackBarState({
                open: true,
                message: "Location contains special characters",
                autoHideDuration: 2000,
                severity: "warning",
            })
        } else {
            setSnackBarState({
                open: true,
                message: "Sending and grading CV!",
                autoHideDuration: null,
                severity: "info",
            })
            const formData = new FormData()

            const blob = new Blob([JSON.stringify(searchQuery)], {
                type: "application/json",
            })

            formData.append("file", uploadedFile)
            formData.append("query", blob)

            const response = await fetch(
                "https://resume-match.herokuapp.com/api/upload",
                {
                    method: "POST",
                    body: formData,
                }
            )

            const status = await response.status
            const data = await response.json()

            if (status === 200) {
                console.log("ARR")
                if (data["data"] && data["data"].length > 0) {
                    setSnackBarState({
                        open: true,
                        message: "Grading success!",
                        autoHideDuration: 1000,
                    })
                    let gradedJobs = data["data"].sort(
                        (job1, job2) => job2.grade - job1.grade
                    )
                    setJobPostings(gradedJobs)
                } else {
                    setSnackBarState({
                        open: true,
                        message: "Problem grading CV :(",
                        autoHideDuration: 1000,
                        severity: "error",
                    })
                }
            } else {
                setSnackBarState({
                    open: true,
                    message: "Problem grading CV :(",
                    autoHideDuration: 1000,
                    severity: "error",
                })
            }
        }
    }

    const setFile = (event) => {
        setUploadedFile(event.target.files[0])
    }

    return (
        <div className="search-section">
            <form
                encType="multipart/form-data"
                className="searchForm"
                noValidate
                autoComplete="off"
            >
                <TextField
                    error={jobSpecialChar}
                    onChange={(event) => updateFormFields(event, "job")}
                    value={searchQuery["job"]}
                    className="textBox"
                    id="job"
                    label="Job"
                    helperText={
                        jobSpecialChar ? "Contains special characters" : ""
                    }
                />
                <TextField
                    error={locationSpecialChar}
                    onChange={(event) => updateFormFields(event, "location")}
                    value={searchQuery["location"]}
                    className="textBox"
                    id="location"
                    label="Location"
                    helperText={
                        locationSpecialChar ? "Contains special characters" : ""
                    }
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
            <Snackbar
                onClose={onClose}
                open={open}
                autoHideDuration={autoHideDuration}
                anchorOrigin={{ vertical: "top", horizontal: "center" }}
            >
                <Alert onClose={onClose} severity={severity}>
                    {message}
                </Alert>
            </Snackbar>
        </div>
    )
}
export default Upload
