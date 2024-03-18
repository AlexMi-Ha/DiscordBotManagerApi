
refreshLists()

function refreshLists() {
    const activeList = document.getElementById('list-active-bots');
    const inactiveList = document.getElementById('list-inactive-bots');

    activeList.innerHTML = spinner();
    inactiveList.innerHTML = spinner();

    fetch('/api/discordbots')
    .then(e => {
        if(!e.ok) {
            displayError("Failed loading the bots!");
            activeList.innerHTML = empty();
            inactiveList.innerHTML = empty();
            disableKillAll();
        }
        return e.json();
    })
    .then(e => {
        activeList.innerHTML = buildBotList(e.filter(e => e.IsRunning === true));
        if(activeList.innerHTML.trim().length == 0) {
            activeList.innerHTML = empty();
            disableKillAll();
        }else {
            disableKillAll(false);
        }
        inactiveList.innerHTML = buildBotList(e.filter(e => e.IsRunning === false));
        if(inactiveList.innerHTML.trim().length == 0) {
            inactiveList.innerHTML = empty();
        }
    })
}

function empty() {
    return '<p class="low-opac">No Bots in this stage!</p>'
}

function spinner() {
    return '<div class="loader"></div>'
}

function setSpinner() {
    const activeList = document.getElementById('list-active-bots');
    const inactiveList = document.getElementById('list-inactive-bots');

    disableKillAll();

    activeList.innerHTML = spinner();
    inactiveList.innerHTML = spinner();
}

function disableKillAll(val = true) {
    document.getElementById('btn-kill-all').disabled = val;
}

function killAll() {
    setSpinner();

    fetch('/api/discordbots/runningbots', {
        method: 'DELETE'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed killing the bots!");
        }
        refreshLists();
    })
}

function runBot(id) {
    setSpinner();

    fetch('/api/discordbots/runningbots/' + id, {
        method: 'POST'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed starting the bot!");
        }
        refreshLists();
    })
}

function killBot(id) {
    setSpinner();

    fetch('/api/discordbots/runningbots/' + id, {
        method: 'DELETE'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed killing the bot!");
        }
        refreshLists();
    })
}

function pullBot(id) {
    setSpinner();

    fetch('/api/discordbots/' + id + '/pull', {
        method: 'POST'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed pulling the bot!");
        }
        refreshLists();
    })
}

function updateBotConfig(id, config) {
    setSpinner();

    const formData = new FormData();
    formData.append('environment', config);

    return fetch('/api/discordbots/' + id + '/config', {
        method: 'POST',
        body: formData
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed updating the bot config!");
        }
        refreshLists();
    })
}

function addBot(githubUrl, botName, botDescription, entryFile, environment) {
    setSpinner();

    const formData = new FormData();
    formData.append('github', githubUrl);
    formData.append('name', botName);
    formData.append('description', botDescription);
    formData.append('entry', entryFile);
    formData.append('environment', environment);

    return fetch('/api/discordbots', {
        method: 'POST',
        body: formData
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed adding the bot!");
        }
        refreshLists();
    })
}

function deleteBot(id) {
    setSpinner();

    fetch('/api/discordbots/' + id, {
        method: 'DELETE'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed deleting the bot!");
        }
        refreshLists();
    })
}

function getBotConfig(id) {
    setSpinner();

    return fetch('/api/discordbots/' + id + '/config', {
        method: 'GET'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed getting the bot config!");
            throw Error;
        }
        return e.json();
    })
}

function displayError(error) {
    document.getElementById('error-content').innerText = error;
    const dialog = document.getElementById('error-dialog');
    dialog.classList.add('active');
    
    setTimeout(() => {
        dialog.classList.add('disposing');
        dialog.classList.remove('active');

        setTimeout(() => {
            dialog.classList.remove('disposing');
        }, 1000)
    }, 2000)
}

const editDialog = document.getElementById('edit-dialog');
const editEnvironment = document.getElementById('edit-environment');
let currentConfigureId = undefined;
let currentlySaving = false;

function configIsValid() {
    return editEnvironment.reportValidity();
}

function openConfigureDialog(id) {
    if(currentlySaving)
        return;
    editEnvironment.value = '';
    getBotConfig(id)
    .then(e => {
        editEnvironment.value = e;
        editDialog.showModal();
        currentConfigureId = id;
    });
}

function cancelConfigureDialog() {
    if(currentlySaving)
        return;

    editDialog.close();
    currentConfigureId = undefined;
    refreshLists();
}

async function saveConfigureDialog() {
    if(currentlySaving) {
        return
    }
    if(!configIsValid()) {
        return;
    }

    currentlySaving = true;
    editDialog.close();
    try {
        await updateBotConfig(currentConfigureId, editEnvironment.value)
    }finally {
        currentConfigureId = undefined;
        currentlySaving = false;
    }
}

const addDialog = document.getElementById('add-dialog');
const addGithub = document.getElementById('add-github');
const addName = document.getElementById('add-botname');
const addDescription = document.getElementById('add-botdescription');
const addEntry = document.getElementById('add-botentry');
const addEnvironment = document.getElementById('add-environment');

function addIsValid() {
    return addGithub.reportValidity() && addName.reportValidity() && addDescription.reportValidity() && addEntry.reportValidity() && addEnvironment.reportValidity();
}

function openAddDialog() {
    if(currentlySaving)
        return;

    addGithub.value = '';
    addName.value = '';
    addDescription.value = '';
    addEntry.value = '';
    addEnvironment.value = '';

    addDialog.showModal();
}

function cancelAddDialog() {
    if(currentlySaving)
        return;

    addDialog.close();
}

async function saveAddDialog() {
    if(currentlySaving)
        return;

    if(!addIsValid()) {
        return;
    } 

    currentlySaving = true;
    addDialog.close();
    try {
        await addBot(addGithub.value, addName.value, addDescription.value, addEntry.value, addEnvironment.value);
    }finally {
        currentlySaving = false;
    }
}

function buildBotList(bots) {
    return bots.map(e => {
        return buildBotContainer(e.Id, e.Name, e.Description, e.IsRunning)
    })
    .join('\n');
}

function buildBotContainer(id, name, description, active) {
    return `
        <div class="bot-panel">
            <div class="bot-title">
                <p><u>${name}</u></p>
                <p>${description}</p>
            </div>
            <div class="bot-info">
                <p class="${active ? 'bot-active-icon' : 'bot-inactive-icon'}"><i class="circle"></i>${active ? 'Active' : 'Inactive'}</p>
            </div>
            <div class="bot-actions">
                ${
                    active ?
                    '<button class="btn btn-kill" onclick="killBot(\''+id+'\')">Kill</button>' :
                    '<button class="btn btn-run" onclick="runBot(\''+id+'\')">Run</button>'
                }
                <button class="btn" onclick="pullBot('${id}')">Pull from Git</button>
                <button class="btn" onclick="openConfigureDialog('${id}')">Configure</button>
                <button class="btn btn-kill" onclick="deleteBot('${id}')">Delete Bot</button>
            </div>
        </div>
    `
}