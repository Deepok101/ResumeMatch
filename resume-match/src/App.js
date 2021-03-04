// import logo from "./logo.svg"
import "./App.css"
import React, { useState, useEffect } from "react"

import Upload from "./components/upload/upload-component"
import PostingsSection from "./components/postingsSection/postingsSection"
import DetailedPosting from "./components/detailedPosting/detailedPosting-component"
import Filter from "./components/filter/filter-component"

function App() {
    const [jobPostings, setJobPostings] = useState([])
    const [selectedJob, setSelectedJob] = useState(null)

    const [filterGrade, setFilterGrade] = React.useState("")
    const [filterDistance, setFilterDistance] = React.useState("")
    const [filterSalary, setFilterSalary] = React.useState(0)

    useEffect(() => {
        setJobPostings([
            {
                title: "Software Dev",
                company: "Microsoft",
                grade: 60,
                description: `Job Description:

Note: By applying to this position your application is automatically submitted to the following locations: Waterloo, ON, Canada; Montreal, QC, Canada
Minimum qualifications:

Bachelor's degree in Computer Science or related technical field, or equivalent practical experience.
Experience working with Data Structures or Algorithms (e.g., data structures/algorithms class, coursework/projects, research, internships, or other practical experience in/outside of school or work (including open source hobby coding).
Software development experience coding in a general purpose programming language.
Examples of coding in one of the following programming languages including but not limited to: C, C++, Java, JavaScript or Python.

Remote interview process
Virtual meetings`,
                location: "Montreal, Qc",
                salary: "28$/hr",
            },
            {
                title: "Web Dev",
                company: "Amazon",
                grade: 70,
                description: `

This position could be located in Montreal or Toronto depending on candidate's preference.

We’re scaling up our algorithmic trading operations and looking for candidates with software development and/or quantitative backgrounds. We sit at the intersection of technology and f

inance, elaborating and implementing novel ways to leverage technology in our automated trading activities.

We’re a small team where each person wears many hats. We rely strongly on software and automation to achieve the kind of impact we’re known for. We pride ourselves on making data-driven decisions and thrive on seeing the immediate impact of those decisions every day.

What you might do in a typical day

Iteratively test and improve the real-time pricing strategy of a particular asset type
Compare merits of different technical approaches and choose which one to use
Evaluate how the latency from geographical topology affects local strategy perspective
The traits that will make you successful in our team

Independent, creative, accountable
Foresee, investigate and fix problems with a logical, systematic, and practical approach
Deliver functionality now while working on long-term technical goals`,
            },
        ])
    }, [])

    function onJobSelect(idx) {
        setSelectedJob(jobPostings[idx])
    }

    return (
        <div>
            <div className="title">Resume Match</div>
            {/* <div className="search-section">
                <form className="searchForm" noValidate autoComplete="off">
                    <TextField className="textBox" id="job" label="Job" />
                    <TextField
                        className="textBox"
                        id="location"
                        label="Location"
                    />
                </form>
                
            </div> */}
            <Upload />
            <Filter
                filterGrade={filterGrade}
                filterDistance={filterDistance}
                filterSalary={filterSalary}
                setFilterGrade={setFilterGrade}
                setFilterDistance={setFilterDistance}
                setFilterSalary={setFilterSalary}
            ></Filter>
            <div className="main">
                <div className="display-postings-section">
                    <PostingsSection
                        jobs={jobPostings}
                        onJobSelect={onJobSelect}
                        filterGrade={filterGrade}
                        filterDistance={filterDistance}
                        filterSalary={filterSalary}
                    />
                </div>
                <div className="display-job-section">
                    <DetailedPosting job={selectedJob} />
                </div>
            </div>
        </div>
    )
}

export default App
