// import logo from "./logo.svg"
import "./App.css"
import { TextField } from "@material-ui/core"
import Parser from "./components/parser/parser-component"
import Upload from './components/upload/upload-component'

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
            <Upload/>
            <Parser></Parser>
        </div>
    )
}

export default App
