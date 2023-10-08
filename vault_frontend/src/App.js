//import './App.css'
import Piece from "./components/Piece"; 
import Controls from "./components/Controls"; 
import React, {useState, useRef, useEffect} from "react";
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
                },
                { 
                        id:896987223, 
                        title: "Raine Fics",
                        url: 'raineficx.png'             
                },

                
        ];
        
    const [renderedPieces, setRenderedPieces] = useState(10);
    const [pieces, setPieces] = useState([]);
    const observerTarget = useRef(null)

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
                setRenderedPieces(10);
                console.log("Got from query: " + jsonResp.length );
            }
        } catch(err) {
            console.log(err)
        }

    }
        
    function createObserver() {
        let observer;

        let options = {
            threshold: 1
        };

        observer = new IntersectionObserver(handleIntersect, options);
        if (observerTarget.current ) {
            observer.observe(observerTarget.current)
        }

        return () => {
            if (observerTarget.current) {
                observer.unobserve(observerTarget.current);
            }
        }
    }

    function handleIntersect(entries, observer) {
        if (entries[0].isIntersecting) {
            setRenderedPieces( pcs => pcs + 10 );
        }
    }

    useEffect(createObserver, [observerTarget]); 
    useEffect(() => {
            console.log("Modified  rendered to: " + renderedPieces)
            },
            [renderedPieces]);

    const pieceList = pieces.slice(0, renderedPieces).map((piece) => (
        <Piece
            id={piece.id}
            title={piece.title}
            url={piece.url}
            thumbnail={piece.thumbnail}
            patreon_url={piece.patreon_url}
        />
    ));
    return (
        <div className="App">
            <div className='columns is-centered'>
                <div className='column is-two-thirds'>
                    <h1 className="title is-1 has-text-centered 
                        has-background-light"> Twokinds ArtVault </h1>
                    <Controls fetchFunc={fetchArt} setFunc={setPieces} />
                </div>
            </div>

            <div className="columns is-centered results-pane">
                <div className='column is-half'>
                    <h2 className='subtitle is-2'>Results</h2>
                </div>
            </div>
            <div className="columns is-centered">
                <div className="column is-two-thirds">
                    <div className="columns is-multiline is-centered">
                        {pieceList}
                        <div ref={observerTarget}></div>
                    </div>
                </div>
            </div>
                
        </div>
    );
}

export default App;
