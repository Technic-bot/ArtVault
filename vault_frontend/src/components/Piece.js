import React from "react";

export default function Piece(props) {
    return (
        <div class='box has-background-light' >
            <p class='title' > {props.title} </p>
            <a href={props.url}>
                <img src={props.thumbnail} alt={props.thumbnail} />
            </a>
        </div>
    )
}
