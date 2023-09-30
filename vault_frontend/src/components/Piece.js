import React from "react";

export default function Piece(props) {
    return (
        <div class="result-item">
            <img src={props.url} alt={props.title} />
        </div>
    )
}
