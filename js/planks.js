
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

        const header = document.createElement("div");
        header.classList.add("top-header");

        const download = document.createElement("a");

        download.classList.add("download");
        download.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"40\" width=\"40\"><path d=\"M9.458 33.333q-1.125 0-1.958-.833t-.833-1.958v-5.625h2.791v5.625h21.084v-5.625h2.791v5.625q0 1.125-.833 1.958t-1.958.833ZM20 26.875l-8.125-8.167 1.958-2 4.792 4.792V6.667h2.75V21.5l4.792-4.792 1.958 2Z\"/></svg>";


        download.href = "data:text/csv;charset=utf-8," + encodeURIComponent(result["csv"]);
        download.download = "planches_" + baseSize + ".csv";

        header.appendChild(download);


        const name = document.createElement("h3");
        name.innerText = "Planche de " + baseSize;

        header.appendChild(name);
        resultContainer.appendChild(header);

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

