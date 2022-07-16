function search(e){
    let query = document.getElementById("query field").value;
    
    if (query != "") {
        console.log(`searching for ${query} ...`);
        const element = document.getElementById("active_video")
        element.innerHTML = "<p class='video-message'>loading video ..</p>"     
        window.location.href = "http://localhost:5000/results";
    }
    else {
        console.log("no query provided");
    }  
}

function directSearch(e){
    e.preventDefault()
    let query = document.getElementById("direct_search_input").value
    let request_url = `http://localhost:5000/direct_search?query=${query}`
    console.log(request_url)
    fetch(request_url).then(response => response.json()).then(response => onDirectSearch(response[query]))
}
document.getElementById("direct-search-form").addEventListener('submit', directSearch);
function onDirectSearch(claim) {
    console.log(claim)
    console.log(claim.name)
    if (claim.hasOwnProperty("error")) {
        document.getElementById("current-vid-title").innerHTML = "Claim not found"
        document.getElementById("active-video").innerHTML = ""
    }
    else {
        // change title 
        title = document.getElementById("current-vid-title")
        try {title.innerHTML = claim.value.title}
        catch(err) {title.innerHTML = "No tile found"}

        // change thumbnail 
        vid_box = document.getElementById("active-video")
        try { vid_box.innerHTML = `<img class="thumbnail main" src=${claim.value.thumbnail.url}>` }
        catch(err) {vid_box.innerHTML = '<p class="video-message">NO THUMBNAIL FOUND</p>'}

        //load video
        console.log("issou")
        if (claim.hasOwnProperty("streaming_url")) {
            console.log("test vid src:",test_vid.getAttribute("src"))
            test_vid = document.querySelector("#test-video")
            test_vid.setAttribute("src",claim.streaming_url)
            console.log("test vid src:",test_vid.getAttribute("src"))
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
document.getElementById("loggin_form").addEventListener('submit', log_in);;


//fetch("http://localhost:5000/nig").then(response => response.json()).then(response => alert(JSON.stringify(response)))
