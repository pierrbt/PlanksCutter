const planksContainer = document.getElementsByClassName("planksContainer")[0];
const planks = document.getElementsByClassName("planks1")[0];
const allPlanks = document.getElementsByClassName("allPlanks");
const addButton = document.getElementsByClassName("addPlank")[0];
const sendButton = document.getElementsByClassName("sendPlanks")[0];

addButton.addEventListener("click", function() {
    const newPlanks = planks.cloneNode(true);
    newPlanks.classList.replace("planks1", "planks" + (allPlanks.length + 1.0))
    newPlanks.getElementsByClassName("plankNumber")[0].innerHTML = "Planche n°" + (allPlanks.length + 1.0);
    planksContainer.appendChild(newPlanks);
    planksContainer.appendChild(addButton);
});
sendButton.addEventListener("click", function() {
    sendButton.innerHTML = "Calcul en cours...";
    const longueurBasePlanche = document.getElementById("longueurBasePlanche").value;
    const planksToSend = [];
    for (let i = 0; i < allPlanks.length; i++) {
        const plank = allPlanks[i];
        const longueurPlanche = plank.getElementsByClassName("plankLength")[0].value;
        const nombrePlanche = plank.getElementsByClassName("plankQty")[0].value;
        planksToSend.push({
            longueurPlanche,
            nombrePlanche
        });
    }
    const send = {
        longueurBasePlanche,
        planksToSend
    }

    fetch("/upload", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(send)
    }).then(res => res.json().then(data => {
        displayPlanks(data);
    }))

    sendButton.innerHTML = "Recalculer";
});