import React, {useState} from "react";

export default function Controls(props) {
    const [title, setTitle] = useState('')
    const [tags, setTags] = useState('')
    const [sort, setSort] = useState('')
    
    function handleSubmit(e) {
        e.preventDefault();
        props.fetchFunc(title, tags, sort);
    }
    function handleTagsChange(e) {
        setTags(e.target.value);
    }
    function handleTitleChange(e) {
        setTitle(e.target.value);
    }
    function handleSortChange(e) {
        setSort(e.target.value);
    }

    return (
        <div className="input-pane">
            <form onSubmit={handleSubmit}>
                <div className='field'>
                    <label className='label is-medium'> Title </label>
                    <div className='control'>
                        <input className='input is-primary'
                         type="text" id="titleQuery"
                         placeholder="Search by title..."
                         value={title}
                         onChange = {handleTitleChange}/>
                    </div>
                </div>
                <div className='field'>
                    <label className='label is-medium'> Tags </label>
                    <div className='control'>
                        <input className='input is-primary' 
                         type="text" id="tagQuery" 
                         placeholder="Search by tags..."
                         value = {tags}
                         onChange = {handleTagsChange}/>
                    </div>
                </div>
                <div className='field'>
                    <label className='label is-normal'> Sort By </label>
                    <div className='select'>
                        <select className='control' onChange = {handleSortChange}>
                            <option value='date_desc'>Date Descending</option>
                            <option value='date_asc'>Date Ascending</option>
                        </select>
                    </div>
                </div>
                <div className='control'>
                    <button className='button is-primary' id="submitBtn">Query</button>
                </div>
            </form>
        </div>
    )
}
