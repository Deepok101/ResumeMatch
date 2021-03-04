import { Paper, Button } from "@material-ui/core"
import React from "react"
import "./detailedPosting-component.css"

import Grade from '../grade/grade-component'

const DetailedPosting = ({ job }) => {

    return (
        <Paper elevation={3} className="detailed-container">
            {job ? (
                <div>
                    <div className="basic-info">
                        <div className="heading">
                            <div>
                                <h2>{job.jobname}</h2>
                                <h3>{job.companyname} &middot; {job.location}</h3>
                                <h3>{job.salary}</h3>
                            </div>
                            <Grade grade={job.grade} />
                        </div>
                        <Button><a href={job.url}>Click here to apply on indeed</a></Button>
                    </div>
                    <div className="description" dangerouslySetInnerHTML={{ __html: job.descrip}}></div>
                </div>
            ) : (
                <></>
            )}
        </Paper>
    )
}

export default DetailedPosting
