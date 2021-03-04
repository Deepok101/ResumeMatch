import React from 'react'
import './grade-component.css'

const Grade = ({grade}) =>{

    let rating;
    if (grade >= 85){
        rating = "great"
    }else if (grade >60 ){
        rating = "medium"
    }
    else {
        rating = "bad"
    }

    return (
   
            <h1 className={"grade "+ rating}>{grade}</h1>

    )

}

export default Grade