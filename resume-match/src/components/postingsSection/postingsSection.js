import React from "react"
import "./postingsSection.css"

import JobCard from "../jobCard/jobCard-component"

const PostingsSection = ({
    jobs,
    onJobSelect,
    filterGrade,
    filterDistance,
    filterSalary,
}) => {
    let job = jobs.map((job, idx) => (
        <div onClick={() => onJobSelect(idx)}>
            {job.grade >= filterGrade ? <JobCard job={job} /> : <></>}
        </div>
    ))

    return <div>{job}</div>
}

export default PostingsSection
