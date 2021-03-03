import React from "react"
import './postingsSection.css'

import JobCard from '../jobCard/jobCard-component'

const PostingsSection = ({ jobs, onJobSelect })=>{
    
    let job = jobs.map( (job,idx) => (
        <div onClick={() => onJobSelect(idx)} >
            <JobCard job={job} />
        </div>
    ))

    return (
        <div>
            {job}
        </div>
    )

}

export default PostingsSection