import React, {useState} from "react";

export default function Controls(props) {
    const [title, setTitle] = useState()
    const [tags, setTags] = useState()
    
    function handleSubmit(e) {
        e.preventDefault();
        props.fetchFunc(title, tags);
    }
    function handleTagsChange(e) {
        setTags(e.target.value);
    }
    function handleTitleChange(e) {
        setTitle(e.target.value);
    }

    return (
        <div class="input-pane">
            <form onSubmit={handleSubmit}>
                <div>
                    <label> Title
                        <input type="text" id="titleQuery"
                         placeholder="Search by title..."
                         value={title}
                         onChange = {handleTitleChange}/>
                    </label>
                </div>
                <div>
                    <label> Tags
                        <input type="text" id="tagQuery" 
                         placeholder="Search by tags..."
                         value = {tags}
                         onChange = {handleTagsChange}/>
                    </label>
                </div>
                <button id="submitBtn">Query</button>
            </form>
        </div>
    )
}
