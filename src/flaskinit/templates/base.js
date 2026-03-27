<meta name="viewport" content="width=device-width, initial-scale=1">
<div id="dynamic-content">
    <!-- This will be replaced by JavaScript -->
</div>
<link rel="stylesheet" href="/static/styles.css">
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("dynamic-content");
    let waitAfterCountdown = false;
    let currentState = "main_menu";

    function waitButtonLabel() {
        return `Wait after countdown: ${waitAfterCountdown ? "ON" : "OFF"}`;
    }

    function getViews() {
        return {
        main_menu: `
            <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="f">
                <button class="menu-button" type="submit">Full run</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="d">
                <button class="menu-button" type="submit">Change detail</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="1">
                <button class="menu-button" type="submit">One run</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="c">
                <button class="menu-button" type="submit">Collect</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="submit">Quit</button>
            </form>
           </div>
        `,
        walking: `
            <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="p">
                <button class="menu-button" type="submit">${waitButtonLabel()}</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="submit">Main menu</button>
            </form>
            </div>
        `,
        shooting: `
             <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="space">
                <button class="menu-button" type="submit">Next</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="p">
                <button class="menu-button" type="submit">${waitButtonLabel()}</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="submit">Main menu</button>
            </form>
            </div>
        `,
        pause: `
             <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="space">
                <button class="menu-button" type="submit">Next</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="submit">Main menu</button>
            </form>
            </div>
            `
        };
    }

    function renderState(nextState) {
        const views = getViews();
        if (!views[nextState]) return;
        currentState = nextState;
        container.innerHTML = views[nextState];
    }

    renderState("main_menu");

    const socket = io();
    //This is here because I had a nightmare debugging the socketio stuff
    console.log('Connecting to Socket.IO...');

    // Listen for UI updates
    socket.on('update_ui', (data) => {
        console.log('Received update_ui:', data);
        if (data.state) {
            waitAfterCountdown = false;
            renderState(data.state);
        }
    });

    document.addEventListener('submit', async (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (!form.action.endsWith('/send_pygame')) return;

        event.preventDefault();
        const formData = new FormData(form);
        const key = formData.get("key");

        if (key === "p") {
            waitAfterCountdown = !waitAfterCountdown;
            renderState(currentState);
        }

        await fetch('/send_pygame', {
            method: 'POST',
            body: formData
        });
    });
});
</script>