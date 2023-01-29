
function isNumeric(str) {
  if (typeof str != "string") return false // we only process strings!
  return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
      !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

function convertToJson() {
  let ignored = false;

  const data = myAppendGrid66.getAllValue();
  const planksData = myAppendGrid33.getAllValue();
  let planks = [];
  let cuts = [];
  let nbr = [];

  for(let each of planksData)
  {
    const thisSize = each["base"];

    if(!isNumeric(thisSize))
    {
      ignored = true;
      continue;
    }

    planks.push(Number(thisSize));
  }

  const min = Math.min(...planks);

  for(let plank of data)
  {
    let thisSize = plank["coupes"];
    let thisQty = plank["nbr"]

    if(!isNumeric(thisQty) || !isNumeric(thisSize))
    {
      ignored = true;
      continue;
    }



    thisSize = Number(thisSize);
    thisQty = Number(thisQty)

    if(thisSize > min)
    {
      ignored = true;
      continue;
    }


    cuts.push(thisSize);
    nbr.push(thisQty);
  }

  let json = {
    "cuts": {
      "sizes": cuts,
      "quantity": nbr
    },
    "planks": planks,
    "cutSize": 2,
    "export" :
        {
          "direct": true,
          "pdf": false,
          "csv": false
        }
  };

  console.log("Planks : ", planks);
  console.log("Cuts : ", cuts);
  console.log("Qty : ", nbr);

  if(ignored)
    alert("Certaines valeurs ont été ignorées car elles n'étaient pas valides !");

  return json;
}





function getEnteredData()
{
  let jsonData = convertToJson(myAppendGrid66, myAppendGrid33);
  console.log(jsonData);
  jsonData = JSON.stringify(jsonData);

}

document.getElementsByClassName("submit")[0].addEventListener("click", getEnteredData);




let myAppendGrid66 = new AppendGrid({
  element: "tblAppendGrid66",
  uiFramework: "bootstrap5",
  iconFramework: "fontawesome5",
  columns: [
    {
      name: "coupes",
      display: "Taille des coupes",
      type: "number"
    },
    {
      name: "nbr",
      display: "Quantité de coupes",
      type: "number"
    }
  ],
  hideButtons: {
    // Hide the move up and move down button on each row
    moveUp: true,
    moveDown: true
  },
  minRowCount: 0,
  rowDragging: false,
});

let myAppendGrid33 = new AppendGrid({
  element: "tblAppendGrid33",
  uiFramework: "bootstrap5",
  iconFramework: "fontawesome5",
  columns: [
    {
      name: "base",
      display: "Taille des planches à découper",
      type: "number"
    }
  ],
  hideButtons: {
    // Hide the move up and move down button on each row
    moveUp: true,
    moveDown: true
  },
  minRowCount: 0,
  rowDragging: false,
});











