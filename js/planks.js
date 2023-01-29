
function displayPlanks(json)
{
    const allPlanks = document.getElementsByClassName("allDisplayedPlanks")[0];
    const solutions = document.getElementsByClassName("solutions")[0];
    const baseSize = json["baseSize"];
    const cutObj = json["objective"];
    const planks = json["planks"];


    allPlanks.innerHTML = "";
    for (let plank of planks)
    {
        const thisContainer = document.createElement("div");
        thisContainer.classList.add("plankContainer")
        const thisPlank = document.createElement("plank");
        const thisQty = document.createElement("qty");
        thisQty.innerText = plank["nbr"].toString() + " x ";
        thisContainer.appendChild(thisQty);
        for(let cut of plank["pattern"])
        {
            const thisCut = document.createElement("cut");
            thisCut.style.width = ((100 * (cut / baseSize)).toFixed(0).toString() + "%");
            const thisLabel = document.createElement("label");
            thisLabel.innerText = cut.toString() + "cm";
            thisCut.appendChild(thisLabel);
            thisPlank.appendChild(thisCut);
        }
        thisContainer.appendChild(thisPlank);
        allPlanks.appendChild(thisContainer);
    }
    solutions.style.display = "flex";
}

