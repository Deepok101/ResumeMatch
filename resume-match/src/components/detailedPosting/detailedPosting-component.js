import React from 'react' 
import './detailedPosting-component.css'

const DetailedPosting = ({job})=>{



    return(
        <div className='detailed-container'>
            { job ?
            <h1>{job.title}</h1>:
            <></> }
        </div>
    )

}

export default DetailedPosting