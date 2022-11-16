// // WOW CSS ANIMATION 

// $(document).ready(function(){
// 	wow = new WOW(
//       {
//         animateClass: 'animated',
//         offset:       100,
//         callback:     function(box) {
//           console.log("WOW: animating <" + box.tagName.toLowerCase() + ">")
//         }
//       }
//     );
//     wow.init();
    
   
//    $(document).ready(function(){
//         $(".dropdown img.flag").addClass("flagvisibility");

//         $(".dropdown dt a").click(function() {
//             $(".dropdown dd ul").toggle();
//         });
                    
//         $(".dropdown dd ul li a").click(function() {
//             let text = $(this).html();
//             $(".dropdown dt a").html(text);
//             $(".dropdown dd ul").hide();
//         });
//         $(document).bind('click', function(e) {
//             let $clicked = $(e.target);
//             if (! $clicked.parents().hasClass("dropdown"))
//                 $(".dropdown dd ul").hide();
//         });
//    });
// });


/*====================*\
|   CAROUSEL + SLIDER   |
\*====================*/
let slideIndex = 1;
let myTimer;
let slideshowContainer;

window.addEventListener("load",function() {
    showSlides(slideIndex);
    myTimer = setInterval(function(){plusSlides(1)}, 6000);
    // KEEP ARROWS PART OF MOUSEENTER PAUSE/RESUME
    slideshowContainer = document.getElementsByClassName('services-inner')[0]; 
    slideshowContainer.addEventListener('mouseenter', pause)
    slideshowContainer.addEventListener('mouseleave', resume)
})

// NEXT AND PREVIOUS CONTROL
function plusSlides(n){
    clearInterval(myTimer);
    if (n < 0){
        showSlides(slideIndex -= 1);
    } else {
    showSlides(slideIndex += 1); 
    }
    // KEEP ARROWS PART OF MOUSEENTER PAUSE/RESUME
    if (n === -1){
        myTimer = setInterval(function(){plusSlides(n + 2)}, 6000);
    } else {
        myTimer = setInterval(function(){plusSlides(n + 1)}, 6000);
    }
}

// Controls the current slide and resets interval if needed
function currentSlide(n){
    clearInterval(myTimer);
    myTimer = setInterval(function(){plusSlides(n + 1)}, 6000);
    showSlides(slideIndex = n);
}

function showSlides(n){
    let i;
    let slides = document.getElementsByClassName("services");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}
// Pause the slider on mouse enter
pause = () => {
    clearInterval(myTimer);
}
//  Resume the slider on mouse leave
resume = () =>{
    clearInterval(myTimer);
    myTimer = setInterval(function(){plusSlides(slideIndex)}, 6000);
}

/*====================*\
|        STATISTICS     |
\*====================*/
let section_counter = document.querySelector('#stats-container');
let sectionCounter = document.querySelector('#stats-container-1');
let counters = document.querySelectorAll('.stats-item .stat');

let CounterObserver = new IntersectionObserver(
    (entries, observer)=>{
        let [entry] = entries;
        if (!entry.isIntersecting) return;

        let speed = 500;
        counters.forEach((counter, index) => {
            function UpdateCounter() {
                const targetNumber = +counter.dataset.target;
                const initialNumber = +counter.innerText;
                const incPercent = targetNumber / speed;
                if (initialNumber < targetNumber) {
                    counter.innerText = Math.ceil(initialNumber + incPercent);
                    setTimeout(UpdateCounter, 40);
                }
            }
            UpdateCounter();

            if (counter.parentElement.style.animation) {
                counter.parentElement.style.animation = "";
            }
            else {
                counter.parentElement.style.animation = `slide-up 0.3s ease forwards 
                ${index / counters.length + 0.5}s`;
            }
        });
    },
    {
    root:null,
    threshold: 0.4,
});

CounterObserver.observe(section_counter);


/*====================*\
|      RECENT D/W       |
\*====================*/
let $parent = $('#sub-name');
let $lis = $parent.children();
setInterval(function() {
    let $clone = $lis.slice();
    while ($clone.length) {
        $parent.append($clone.splice(Math.floor(Math.random() * $clone.length), 1));
    }
}, 5000);

let $parent1 = $('#sub-amount');
let $lis1 = $parent1.children();
setInterval(function() {
    let $clone = $lis1.slice();
    while ($clone.length) {
        $parent1.append($clone.splice(Math.floor(Math.random() * $clone.length), 1));
    }
}, 5000);

let $parent2 = $('#withdraw-name');
let $lis2 = $parent2.children();
setInterval(function() {
    let $clone = $lis2.slice();
    while ($clone.length) {
        $parent2.append($clone.splice(Math.floor(Math.random() * $clone.length), 1));
    }
}, 5000);

let $parent3 = $('#withdraw-amount');
let $lis3 = $parent3.children();
setInterval(function() {
    let $clone = $lis3.slice();
    while ($clone.length) {
        $parent3.append($clone.splice(Math.floor(Math.random() * $clone.length), 1));
    }
}, 5000);


// REMOVE G-TRANSLATE LOGO AND TEXT
$(window).load(function() {
    $(".goog-logo-link").empty();
    $('.goog-te-gadget').html($('.goog-te-gadget').children());
})
