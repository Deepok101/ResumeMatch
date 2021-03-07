// import logo from "./logo.svg"
import "./App.css"
import React, { useState, useEffect } from "react"
import { Pagination } from "@material-ui/lab"

import Upload from "./components/upload/upload-component"
import PostingsSection from "./components/postingsSection/postingsSection"
import DetailedPosting from "./components/detailedPosting/detailedPosting-component"
import Filter from "./components/filter/filter-component"

function App() {



    const [jobPostings, setJobPostings] = useState([])
    const [selectedJob, setSelectedJob] = useState(null)
    const [displayableJobs, setDisplayableJobs] = useState([])

    const [filterGrade, setFilterGrade] = React.useState("")
    const [filterDistance, setFilterDistance] = React.useState("")
    const [filterSalary, setFilterSalary] = React.useState(0)
    const [showFilter, setShowFilter] = React.useState(false)

    const [pageNumber, setPageNumber] = useState(1)

    const numJobsPerPage = 6

    useEffect(() => {
        // TODO: use filters to update displayable jobs
        setDisplayableJobs(jobPostings)
    }, [jobPostings])

    function onJobSelect(idx) {
        setSelectedJob(jobPostings[idx])
    }

    function onPageSelect(event, pageNum) {
        setPageNumber(pageNum)
    }

    return (
        <div>
            <div className="titleBox">
                <span className="title">Resume Match</span>
            </div>
            <Upload 
                setJobPostings={setJobPostings}
                setShowFilter={setShowFilter} />
            <Filter
                filterGrade={filterGrade}
                filterDistance={filterDistance}
                filterSalary={filterSalary}
                setFilterGrade={setFilterGrade}
                setFilterDistance={setFilterDistance}
                setFilterSalary={setFilterSalary}
                setDisplayableJobs={setDisplayableJobs}
                displayableJobs={displayableJobs}
                jobPostings={jobPostings}
                showFilter={showFilter}
            ></Filter>
            <div className="main">
                <div className="display-data">
                    <div className="display-postings-section">
                        <PostingsSection
                            onJobSelect={onJobSelect}
                            displayableJobs={displayableJobs}
                            pageNumber={pageNumber}
                            numJobsPerPage={numJobsPerPage}
                        />
                    </div>
                    <div className="display-job-section">
                        <DetailedPosting job={selectedJob} />
                    </div>
                </div>
                <Pagination
                    onChange={onPageSelect}
                    count={displayableJobs.length > 0 ? Math.ceil(displayableJobs.length / numJobsPerPage) : 1}
                    shape="rounded"
                />
            </div>
        </div>
    )
}

export default App
