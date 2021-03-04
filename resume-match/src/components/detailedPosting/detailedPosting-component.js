import { Paper } from "@material-ui/core"
import React from "react"
import "./detailedPosting-component.css"

const DetailedPosting = ({ job }) => {
    return (
        <Paper elevation={3} className="detailed-container">
            {job ? (
                <div>
                    <h2>{job.title}</h2>
                    <h3>{job.company}</h3>
                    <div>{job.description}</div>
                </div>
            ) : (
                <></>
            )}
        </Paper>
    )
}

export default DetailedPosting
