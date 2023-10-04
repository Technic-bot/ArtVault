import React from "react";
import patreon_logo from './patreon-logo.png' 

export default function Piece(props) {
    return (
        <div class='column is-one-quarter box has-background-lighti has-text-centered' >
            <p class='title' > {props.title} </p>
            <figure class='is-inline-block'>
                <a href={props.url}>
                    <img src={props.thumbnail} alt={props.thumbnail} />
                </a>
            </figure>
            <div class='columns'>
                <div class='column has-text-centered'>
                    <figure class='is-inline-block'>
                        <a href={props.patreon_url}>
                            <img class='image is-64x64' 
                                src={patreon_logo} alt="Patreon source" />
                        </a>
                    </figure>
                </div>
            </div>
        </div>
    )
}
