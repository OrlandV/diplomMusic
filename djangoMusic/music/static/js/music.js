 function helpClick(obj) {
    const el = document.getElementById(obj);
    el.style.display = el.style.display === 'none' ? '' : 'none';
}

function addTR(ri) {
    const arrOptVal = [""];
    const arrOptTex = [""];
    const ss1 = document.getElementById('selSort');
    const frmSort = document.forms['frmSort'];


    for (let i = 1; i < ss1.children.length; i++) {
        arrOptVal[i] = ss1.children[i].value;
        arrOptTex[i] = ss1.children[i].text;
    }

    // Фильтрация выбранных опций
    for (let i = 0; i < ri; i++) {
        const selectedValue = frmSort[i * 2].value;
        const index = arrOptVal.indexOf(selectedValue);
        if (index > -1) {
            arrOptVal.splice(index, 1);
            arrOptTex.splice(index, 1);
        }
    }

    // Создание нового ряда таблицы
    const tab = frmSort.querySelector('tbody');
    const newTR = tab.insertRow();
    const newTD0 = newTR.insertCell();
    const newTD1 = newTR.insertCell();
    const newSel = document.createElement("SELECT");

    newSel.id = "selSort" + ri;
    newSel.name = newSel.id;
    newSel.setAttribute("onchange", "selChange('" + newSel.id + "');");
    newTD0.appendChild(newSel);

    arrOptVal.forEach((val, i) => {
        const newOpt = document.createElement("OPTION");
        newOpt.value = val;
        newOpt.text = arrOptTex[i];
        newSel.add(newOpt);
    });

    const newChb = document.createElement("INPUT");
    newChb.type = "checkbox";
    newChb.id = "chbSort" + ri;
    newChb.className = "chbSort";
    newTD1.appendChild(newChb);

    const newLab = document.createElement("LABEL");
    newLab.htmlFor = newChb.id;
    newLab.className = "lblSort";
    newLab.textContent = "↓";
    newTD1.appendChild(newLab);
}

function delTR(ri, li) {
    const frmSort = document.forms['frmSort'];
    for (let i = li; i > ri; i--) {
        frmSort.querySelector('tbody').lastElementChild.remove();
    }
}

function selChange(objId) {
    const frmSort = document.forms['frmSort'];
    const sel = document.getElementById(objId);
    const ri = sel.closest('tr').rowIndex;
    const li = frmSort.querySelector('tbody').lastElementChild.rowIndex;

    if (sel.value && ri === li) {
        addTR(ri + 1);
    } else if (!sel.value && ri < li) {
        delTR(ri, li);
    }
}