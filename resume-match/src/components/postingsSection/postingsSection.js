import React from "react"
import './postingsSection.css'

import JobCard from '../jobCard/jobCard-component'

const PostingsSection = ({ jobs })=>{
    
    let job = jobs.map( job => (
        <div>
            <JobCard job={job}/>
        </div>
    ))

    return (
        <div>
            {job}
        </div>
    )

}

export default PostingsSection