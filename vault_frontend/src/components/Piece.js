import React from "react";

export default function Piece(props) {
    return (
        <div class="result-item">
            <p> {props.title} </p>
            <img src={props.url} alt={props.title} />
        </div>
    )
}
