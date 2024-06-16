//import './App.css'
import Piece from "./components/Piece"; 
import Controls from "./components/Controls"; 
import React, {useState, useRef, useEffect} from "react";
import 'bulma/css/bulma.min.css';

function App() {
    const [renderedPieces, setRenderedPieces] = useState(0);
    const [pieces, setPieces] = useState([]);
    const observerTarget = useRef(null)
    const piecesRef = useRef(null)
    const renderedRef = useRef(null)
    piecesRef.current = pieces;
    renderedRef.current = renderedPieces;

    async function fetchArt(title, tags, sorting) {
        try {
            var sort_order;
            if (sorting == 'date_asc') {
                sort_order = 'asc';
            } else {
                sort_order = 'desc';
            }

            const endpoint = '/artworks/search?';
            if (!title && !tags) {
                return;
            }
            const params = new URLSearchParams({
                title: title,
                tags: tags,
                sorting: sort_order
            });
            const response = await fetch(endpoint + params);

            if (response.ok) {
                const jsonResp = await response.json();
                setPieces(jsonResp);
                setRenderedPieces(10);
                //console.log("Got from query: " + jsonResp.length );
            }
        } catch(err) {
            console.log(err)
        }

    }
    
    async function fetchLatestArt( limit) {
        try {
            const endpoint = '/artworks/latest?';
            const params = new URLSearchParams({
                limit: limit
            });
            const response = await fetch(endpoint + params);

            if (response.ok) {
                const jsonResp = await response.json();
                setPieces(jsonResp);
                setRenderedPieces(10);
            }
        } catch(err) {
            console.log(err)
        }

    }
    useEffect(() => {
        fetchLatestArt(32);        
    }, []);
        
    function createObserver() {
        let observer;

        let options = {
            threshold: 0.75,
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
        //console.log("Rendering " + renderedRef.current+" from " + piecesRef.current.length);
        if (piecesRef.current.length > renderedRef.current) {
            setRenderedPieces( pcs => pcs + 8 );
        }
    }

    useEffect(createObserver, [observerTarget]); 
    const allDone = pieces.length && (renderedPieces >= pieces.length);
    //console.log("Rendering " + renderedPieces +" from " + piecesRef.current.length);

    let endMsg = <div></div>;
    if (allDone) {
        endMsg = (<div className="columns is-centered"> 
           <div className='box is-1 column is-one-quarter has-text-centered '>
                <h1 className='subtitle is-3'> All Art Fetched </h1>
            </div>
       </div>);
    }

    const pieceList = pieces.slice(0, renderedPieces).map((piece) => (
        <Piece
            id={piece.id}
            title={piece.title}
            url={piece.url}
            thumbnail={piece.thumbnail}
            patreon_url={piece.patreon_url}
            date={piece.date}
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
                    </div>
                </div>
            </div>
            <div className="columns is-centered" ref={observerTarget}>
		<div className='box is-1 column is-one-quarter has-text-centered '>
		    <button onClick={handleIntersect} className="button is-primary"
			    id="loadBtn" disabled={allDone}> Load More </button>
               </div>
            </div>
            {endMsg}
                
        </div>
    );
}

export default App;
