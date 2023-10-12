//import './App.css'
import Piece from "./components/Piece"; 
import Controls from "./components/Controls"; 
import React, {useState, useRef, useEffect} from "react";
import 'bulma/css/bulma.min.css';

function App() {
    const [renderedPieces, setRenderedPieces] = useState(10);
    const [pieces, setPieces] = useState([]);
    const observerTarget = useRef(null)
    const piecesRef = useRef(null)
    piecesRef.current = pieces;

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
                setRenderedPieces(8);
                //console.log("Got from query: " + jsonResp.length );
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
            if (piecesRef.current.length > renderedPieces) {
                setRenderedPieces( pcs => pcs + 10 );
                // console.log("Rendering " + renderedPieces +" from " + piecesRef.current.length);
            }
        }
    }

    useEffect(createObserver, [observerTarget]); 
    const allDone = pieces.length && (renderedPieces >= pieces.length);
    //console.log("Rendering " + renderedPieces +" from " + piecesRef.current.length);

    const pieceList = pieces.slice(0, renderedPieces).map((piece) => (
        <Piece
            id={piece.id}
            title={piece.title}
            url={piece.url}
            thumbnail={piece.thumbnail}
            patreon_url={piece.patreon_url}
        />
    ));

    let resultSentence = '';
    if (pieces.length) {
        resultSentence = "Got " + pieces.length + " artworks";
    } else {
        resultSentence = "";
    }

    return (
        <div className="App mx-1">
            <div className='columns is-centered'>
                <div className='box column is-two-thirds'>
                    <div className='box has-background-light'>
                        <h1 className="title is-1 has-text-centered">
                         Twokinds ArtVault 
                         </h1>
                    </div>
                    <Controls fetchFunc={fetchArt} setFunc={setPieces} />
                </div>
            </div>

            <div className="columns is-centered results-pane">
                { resultSentence &&
                <div className='column is-half'>
                    <h2 className='box subtitle is-2'>Results: {resultSentence}</h2>
                </div>
                }
            </div>
            <div className="columns is-centered">
                <div className="column is-two-thirds">
                    <div className="columns is-multiline is-centered">
                        {pieceList}
                        <div ref={observerTarget}></div>
                    </div>
                </div>
            </div>
            {allDone &&
               <div className="columns is-centered"> 
                   <div className='box is-1 column is-one-quarter
                        has-text-centered '>
                        <h1 className='subtitle is-3'> All Art Fetched </h1>
                    </div>
               </div>
            }
                
        </div>
    );
}

export default App;
