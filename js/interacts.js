isIn = false;
function addTheInteractions()
{
    const allTheFuckingPlanks = document.getElementsByTagName("plank");
    for(let i = 0; i < allTheFuckingPlanks.length; i++)
    {
        allTheFuckingPlanks[i].addEventListener("mouseover", function(event) {
            isIn = (event.target.tagName !== "CUT" && event.target.tagName !== "LABEL");
        });
        allTheFuckingPlanks[i].addEventListener("mouseout", function(event) {
            isIn = false;
        });
    }
    setInterval(function() {
        console.log(isIn);
    }, 100);
}


