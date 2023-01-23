json = {
    "baseSize": 2410,
    "objective": 10,
    "planks": [
        {
            nbr: 2,
            pattern: [1600, 600, 200, 250]
        },
        {
            nbr: 3,
            pattern: [2000, 500]
        },
        {
            nbr: 5,
            pattern: [320, 560, 1000, 400, 320]
        }
    ]
}
const allPlanks = document.getElementsByClassName("allDisplayedPlanks")[0];
const baseSize = json["baseSize"];
const cutObj = json["objective"];
const planks = json["planks"];

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
        thisCut.style.width = ((80 * (cut / baseSize)).toFixed(0).toString() + "%");
        const thisLabel = document.createElement("label");
        thisLabel.innerText = cut.toString() + "cm";
        thisCut.appendChild(thisLabel);
        thisPlank.appendChild(thisCut);
    }
    thisContainer.appendChild(thisPlank);
    allPlanks.appendChild(thisContainer);
}