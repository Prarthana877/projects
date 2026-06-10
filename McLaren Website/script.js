// Toggle the menu icon and expand/collapse the navigation links.
function toggleMenu(){
    const menu=document.querySelector(".menu");
    const nav = document.querySelector(".nav");
    menu.classList.toggle("active");
    nav.classList.toggle("active");
} 

// Change the active background video, trailer preview, and model title.
function changeVideo(name){
    // Collect the elements that share matching McLaren model classes.
    const bgVideoList=document.querySelectorAll(".bg-video");
    const trailers=document.querySelectorAll(".trailer");
    const models=document.querySelectorAll(".model");

    // Show only the background video that matches the selected model.
    bgVideoList.forEach(video=>{
        video.classList.remove("active");
        if(video.classList.contains(name)){
            video.classList.add("active");
        }
    })

    // Show only the model heading that matches the selected model.
    models.forEach(models=>{
        models.classList.remove("active");
        if(models.classList.contains(name)){
            models.classList.add("active");
        }
    })

    // Show only the trailer video that matches the selected model.
    trailers.forEach(video=>{
        trailers.classList.remove("active");
        if(trailers.classList.contains(name)){
            trailers.classList.add("active");
        }
    })
}

