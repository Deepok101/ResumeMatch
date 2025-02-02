import { Paper, Button } from "@material-ui/core"
import React from "react"
import "./detailedPosting-component.css"

import Grade from "../grade/grade-component"

const DetailedPosting = ({ job }) => {
    return (
        <div className="detailed-container">
            {job !== null && job !== undefined ? (
                <Paper elevation={3} className="detailed-container">
                    <div>
                        <div className="basic-info">
                            <div className="heading">
                                <div>
                                    <h2>{job.jobname}</h2>
                                    <h3>
                                        {job.companyname} &middot;{" "}
                                        {job.location}
                                    </h3>
                                    <h3 className="salaryHeader">
                                        {job.salary}
                                    </h3>
                                </div>
                                <Grade grade={job.grade} />
                            </div>
                            <Button
                                className="applyButton"
                                variant="contained"
                                color="primary"
                                href={job.url}
                                target="_blank"
                            >
                                Click here to apply on linkedin
                            </Button>
                        </div>
                        <div
                            className="description"
                            dangerouslySetInnerHTML={{ __html: job.descrip }}
                        ></div>
                    </div>
                </Paper>
            ) : (
                <></>
            )}
        </div>
    )
}

export default DetailedPosting
