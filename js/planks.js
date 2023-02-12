
function displayPlanks(json)
{
    const allPlanks = document.getElementsByClassName("allDisplayedPlanks")[0];
    const solutions = document.getElementsByClassName("solutions")[0];

    allPlanks.innerHTML = "";

    const results = json["results"];

    for(const [key, result] of Object.entries(results))
    {
        const resultContainer = document.createElement("div");
        resultContainer.classList.add("resultContainer");

        const baseSize = key;

        const name = document.createElement("h3");
        name.innerText = "Planche de " + baseSize;
        resultContainer.appendChild(name);

        const { patterns, quantity, statistics } = result;

        for(let i = 0; i < patterns.length; i++)
        {
            const thisContainer = document.createElement("div");
            thisContainer.classList.add("plankContainer")
            const thisPlank = document.createElement("plank");
            const thisQty = document.createElement("qty");

            thisQty.innerText = quantity[i] + " x ";

            thisContainer.appendChild(thisQty);

            for(let cut of patterns[i])
            {
                const thisCut = document.createElement("cut");
                thisCut.style.width = ((100 * (cut / baseSize)).toFixed(0).toString() + "%");
                const thisLabel = document.createElement("label");
                thisLabel.innerText = cut.toString();
                thisCut.appendChild(thisLabel);
                thisPlank.appendChild(thisCut);
            }

            thisContainer.appendChild(thisPlank);
            resultContainer.appendChild(thisContainer);
        }

        const thisStats = document.createElement("stats");
        const thisObj = document.createElement("obj");
        thisObj.innerText = statistics["objective"] + " planches requises";
        thisStats.appendChild(thisObj);
        const thisSizes = document.createElement("sizes");
        thisSizes.innerText = statistics["net"] + " / " + statistics["brut"] + " utilisés";
        thisStats.appendChild(thisSizes);
        const thisWaste = document.createElement("waste");
        thisWaste.innerText = statistics["loss_unit"] + " (" + statistics["loss_percent"] + "%) de perte";
        thisStats.appendChild(thisWaste);

        resultContainer.appendChild(thisStats);

        allPlanks.appendChild(resultContainer);

    }

    solutions.style.display = "flex";
}

