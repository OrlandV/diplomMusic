 function helpClick(obj) {
    const el = document.getElementById(obj);
    el.style.display = el.style.display === 'none' ? '' : 'none';
}

function addTR(ri) {
    let arrOptVal = [""];
    let arrOptTex = [""];
    const ss1 = document.getElementById('selSort');
    const frmSort = document.forms['frmSort'];


    for (let i = 1; i < ss1.children.length; i++) {
        arrOptVal[i] = ss1.children[i].value;
        arrOptTex[i] = ss1.children[i].text;
    }

    // Фильтрация выбранных опций
    let c = 0;
    for (let a = 1; a <= arrOptVal.length - 1; a++) {
        for (let i = 0; i < ri; i++) {
            if (frmSort[i * 2 + 1].value === arrOptVal[a]) {
                arrOptVal.splice(a, 1);
                arrOptTex.splice(a, 1);
                a--;
                c++;
                break;
            }
        }
        if (c === ri) break;
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
        newOpt.id = "selSort" + ri + "Opt" + i;
        newOpt.name = newOpt.id;
        newOpt.value = val;
        newOpt.text = arrOptTex[i];
        newSel.add(newOpt);
    });

    const newChb = document.createElement("INPUT");
    newChb.type = "checkbox";
    newChb.id = "chbSort" + ri;
    newChb.name = newChb.id
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
    const selCount = frmSort[1].childElementCount - 2;
    const sel = document.getElementById(objId);
    const ri = sel.parentNode.parentNode.rowIndex;
    const li = frmSort.querySelector('tbody').lastElementChild.rowIndex;

    if (sel.value && ri === li && ri < selCount) {
        addTR(ri + 1);
    } else if (!sel.value && ri < li) {
        delTR(ri, li);
    } else if (ri < li) {
        delTR(ri, li);
        addTR(ri + 1);
    }
}