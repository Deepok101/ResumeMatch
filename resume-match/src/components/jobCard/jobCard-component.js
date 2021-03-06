import { Paper } from "@material-ui/core"
import React from "react"
import "./jobCard-component.css"

import Grade from '../grade/grade-component'

const JobCard = ({ job }) => {
    return (
        <Paper elevation={3} className="card-border">
            <div className="jobTitleArea">
                <h2 className="job-title">{job.jobname}</h2>
                <Grade grade={job.grade} />
            </div>
            <div>
                <h3 className="job-company">{job.companyname}</h3>
                <div className="basic-req">{job.basicreq}</div>
                <div className="bonusreq">{job.bonusreq}</div>
            </div>

            
        </Paper>
    )
}
export default JobCard
