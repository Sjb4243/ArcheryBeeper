<div id="dynamic-content">
    <!-- This will be replaced by JavaScript -->
</div>

<!-- Load Socket.IO first -->
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("dynamic-content");

    // Dictionary of HTML for different states
    const views = {
        main_menu: `
            <form action="/send_pygame" method="post">
                <input type="hidden" name="key" value="f">
                <button type="submit">Full run</button>
            </form>
            <form action="/send_pygame" method="post">
                <input type="hidden" name="key" value="d">
                <button type="submit">Change detail</button>
            </form>
        `,
        walking: `
            <form action="/send_pygame" method="post">
                <input type="hidden" name="key" value="p">
                <button type="submit">Pause</button>
            </form>
            <form action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button type="submit">Main menu</button>
            </form>
        `
    };

    // Set initial view
    container.innerHTML = views.main_menu;

    // Initialize Socket.IO
    const socket = io();
    console.log('Connecting to Socket.IO...');

    // Listen for UI updates
    socket.on('update_ui', (data) => {
        console.log('Received update_ui:', data);
        if (data.state && views[data.state]) {
            container.innerHTML = views[data.state];
        }
    });

    // Handle form submissions via fetch
    document.addEventListener('submit', async (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (!form.action.endsWith('/send_pygame')) return;

        event.preventDefault();
        const formData = new FormData(form);

        await fetch('/send_pygame', {
            method: 'POST',
            body: formData
        });
    });
});
</script>