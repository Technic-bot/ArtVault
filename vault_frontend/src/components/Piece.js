import React from "react";
import patreon_logo from './patreon-logo.png' 

export default function Piece(props) {
    return (
        <div className='column is-one-quarter box has-background-lighti has-text-centered' >
            <p className='title' > {props.title} </p>
            <figure className='is-inline-block'>
                <a href={props.url}>
                    <img src={props.thumbnail} alt={props.thumbnail} />
                </a>
            </figure>
            <div className='columns'>
                <div className='column has-text-centered'>
                    <figure className='is-inline-block'>
                        <a href={props.patreon_url}>
                            <img className='image is-64x64' 
                                src={patreon_logo} alt="Patreon source" />
                        </a>
                    </figure>
                </div>
            </div>
        </div>
    )
}
