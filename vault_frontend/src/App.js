//import './App.css'
import Piece from "./components/Piece"; 
import Controls from "./components/Controls"; 
import React, {useState} from "react";
import 'bulma/css/bulma.min.css';

function App() {
    const dummy_json = 
        [ 
                { 
                        id:89896118, 
                        title: "Reni's Reliquary",
                        url: 'renismagichorde.png'             
                },
                { 
                        id:89698722, 
                        title: "Bad lifehacks",
                        url: 'lifehacks.png'             
                }
                
        ];
        
    const [pieces, setPieces] = useState(dummy_json);

    async function fetchArt(title, tags) {
        try {
            if (!title && !tags) {
                return;
            }
            const baseUrl = '/artworks/search?';
            const params = new URLSearchParams({
                title: title,
                tags: tags        
            });
            const response = await fetch(baseUrl + params);

            if (response.ok) {
                const jsonResp = await response.json();
                setPieces(jsonResp);
            }
        } catch(err) {
            console.log(err)
        }

    }
        

    const pieceList = pieces.map((piece) => (
        <Piece
            id={piece.id}
            title={piece.title}
            url={piece.url}
            thumbnail={piece.thumbnail}
        />
    ));
    return (
        <div className="App">
            <div class='columns is-centered'>
                <div class='column is-half'>
                    <h1 class="title is-1 has-text-centered 
                        has-background-light"> Twokinds ArtVault </h1>
                    <Controls fetchFunc={fetchArt} setFunc={setPieces} />
                </div>
            </div>

            <div class="columns is-centered results-pane">
                <div class='column is-half'>
                    <h2 class='subtitle is-2'>Results</h2>
                </div>
            </div>
            <div class="columns is-multiline is-centered results-pane">
                <div class='column is-two-thirds has-text-centered'>
                    {pieceList}
                </div>
            </div>
                
        </div>
    );
}

export default App;
