import { Paper } from "@material-ui/core"
import React from "react"
import "./jobCard-component.css"

const JobCard = ({ job }) => {
    return (
        <Paper elevation={3} className="card-border">
            <div className="jobTitleArea">
                <h2 className="job-title">{job.title}</h2>
                <h1 className="grade">{job.grade}</h1>
            </div>
            <h3 className="job-company">{job.company}</h3>
        </Paper>
    )
}
export default JobCard
