// import logo from "./logo.svg"
import "./App.css"
import { Button, TextField } from "@material-ui/core"

function App() {
    return (
        // <div className="App">
        //     <header className="App-header">
        //         <img src={logo} className="App-logo" alt="logo" />
        //         <p>
        //             Edit <code>src/App.js</code> and save to reload.
        //         </p>
        //         <a
        //             className="App-link"
        //             href="https://reactjs.org"
        //             target="_blank"
        //             rel="noopener noreferrer"
        //         >
        //             Learn React
        //         </a>
        //     </header>
        // </div>
        <div>
            <div className="title">Resume Match</div>
            <form className="searchForm" noValidate autoComplete="off">
                <TextField className="textBox" id="job" label="Job" />
                <TextField className="textBox" id="location" label="Location" />
                <TextField className="textBox" id="grader" label="Grade" />
            </form>
            <div className="searchForm">
                <label for="fileUpload" class="fileUploadLabel">
                    Drag and drop to upload your Resume
                </label>
                <input type="file" id="fileUpload" />
                <Button variant="contained" color="primary">
                    Search Button
                </Button>
            </div>
        </div>
    )
}

export default App
