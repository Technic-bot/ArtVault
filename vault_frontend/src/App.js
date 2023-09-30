import './App.css'
import Piece from "./components/Piece"; 
import Controls from "./components/Controls"; 
import React, {useState} from "react";

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
            const baseUrl = '/artworks/search?';
            const params = new URLSearchParams({
                title: title,
                tags: tags        
            });
            console.log(baseUrl + params);
            const response = await fetch(baseUrl + params);

            if (response.ok) {
                const jsonResp = await response.json();
                // Maybe issue here
                console.log(jsonResp);
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
        />
    ));
    return (
        <div className="App">
                <h1> Twokinds ArtVault </h1>
                <Controls fetchFunc={fetchArt} setFunc={setPieces} />
                <div class="results-pane">
                        <h2>Results</h2>
                        <div id="resultsContainer">
                            {pieceList}
                        </div>
                </div>
                
        </div>
    );
}

export default App;
