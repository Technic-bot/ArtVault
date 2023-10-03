import React, {useState} from "react";

export default function Controls(props) {
    const [title, setTitle] = useState('')
    const [tags, setTags] = useState('')
    
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
                <div class='field'>
                    <label class='label is-medium'> Title </label>
                    <div class='control'>
                        <input class='input is-primary'
                         type="text" id="titleQuery"
                         placeholder="Search by title..."
                         value={title}
                         onChange = {handleTitleChange}/>
                    </div>
                </div>
                <div class='field'>
                    <label class='label is-medium'> Tags </label>
                    <div class='control'>
                        <input class='input is-primary' 
                         type="text" id="tagQuery" 
                         placeholder="Search by tags..."
                         value = {tags}
                         onChange = {handleTagsChange}/>
                    </div>
                </div>
                <div class='field'>
                    <button class='button is-primary' id="submitBtn">Query</button>
                </div>
            </form>
        </div>
    )
}
