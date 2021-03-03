import React from "react"
import './jobCard-component.css'

const JobCard = ({job}) => {



    return (
        <div className="card-border">
            <h1 className='job-title'>{job.title}</h1>
            <p className='description'>{job.description}</p>
        </div>
    )

}
export default JobCard