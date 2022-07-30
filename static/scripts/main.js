function search(e){
    let query = document.getElementById("query-field").value; 

    if (query.length >= 3 ) {
        console.log(`searching for ${query} ...`); 
    }
    else {
        alert("query need to be at least 3 characters long")
        console.log("query needs to be at least 3 character to complie with 'https://lighthouse.lbry.com/search' api");
        e.preventDefault();
    }  
}
document.getElementById("search-bar").addEventListener('submit', search);

function directSearch(e){
    e.preventDefault()
    let query = document.getElementById("direct_search_input").value
    if (query) {
        let request_url = `http://localhost:5000/direct_search?query=${query}`
        console.log(request_url)
        fetch(request_url).then(response => response.json()).then(response => onDirectSearchResult(response))
    }
}
if (document.getElementById('direct-search-form')) document.getElementById("direct-search-form").addEventListener('submit', directSearch);

function onDirectSearchResult(claim) {
    console.log(claim)
    if (claim.hasOwnProperty("code")) {
        document.getElementById("current-vid-title").innerHTML = "Claim not found"
        document.getElementById("active-media-container").innerHTML = ""
    }
    else {
        // change title 
        title = document.getElementById("current-vid-title")
        try {title.innerHTML = claim.metadata.title}
        catch(err) {title.innerHTML = "No tile found"}

        content_box = document.getElementById("main-media")
        //load video
        if (claim.hasOwnProperty("streaming_url")) {
            content_box.innerHTML = `
            <video id="main-video" width="1000" height="650" controls>
                <source src=${claim.streaming_url} type="video/mp4">
                <source src=${claim.streaming_url} type="video/ogg">
                video format not supported by your browser
            </video>`
            //set thumbnail
            document.getElementById("main-video").setAttribute("poster",claim.metadata.thumbnail.url) 
            
        }
    }
}
function log_in(event) { 
    event.preventDefault() 
    console.log("feature not yet implemented")
    alert("this feature is not yet implemented")
    //let loggin_header = document.querySelector("#loggin_header")
    //loggin_header.insertAdjacentHTML("afterend","<p style='color: red; font-size : 12px'>this feature is not yet implemented</p>")

 } 
document.getElementById("loggin-form").addEventListener('submit', log_in);;


//fetch("http://localhost:5000/nig").then(response => response.json()).then(response => alert(JSON.stringify(response)))
