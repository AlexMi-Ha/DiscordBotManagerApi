
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

    fetch('/api/discordbots', {
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

    fetch('/api/discordbots/' + id, {
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

    fetch('/api/discordbots/' + id, {
        method: 'DELETE'
    })
    .then(e => {
        if(!e.ok) {
            displayError("Failed killing the bot!");
        }
        refreshLists();
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
                    '<button class="btn btn-kill" onclick="killBot('+id+')">Kill</button>' :
                    '<button class="btn btn-run" onclick="runBot('+id+')">Run</button>'
                }
            </div>
        </div>
    `
}