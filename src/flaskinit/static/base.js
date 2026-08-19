document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("dynamic-content");
    window._clientLogs = window._clientLogs || [];
    ['log','info','warn','error'].forEach(level => {
        const orig = console[level];
        console[level] = function(...args) {
            try { window._clientLogs.push({level, args: args.map(a=>String(a)), ts: Date.now()}); } catch (e) {}
            orig.apply(console, args);
        };
    });
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
                <button class="menu-button" type="button">Full run</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="d">
                <button class="menu-button" type="button">Change detail</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="1">
                <button class="menu-button" type="button">One run</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="c">
                <button class="menu-button" type="button">Collect</button>
            </form>
            <form class="menu-form" action="/control_music" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="button">Play/Pause music</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="button">Quit</button>
            </form>
           </div>
        `,
        walking: `
            <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="p">
                <button class="menu-button" type="button">${waitButtonLabel()}</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="button">Main menu</button>
            </form>
            </div>
        `,
        shooting: `
             <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="space">
                <button class="menu-button" type="button">Next</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="p">
                <button class="menu-button" type="button">${waitButtonLabel()}</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="button">Main menu</button>
            </form>
            </div>
        `,
        pause: `
             <div class="button-container">
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="space">
                <button class="menu-button" type="button">Paused: Press to continue</button>
            </form>
            <form class="menu-form" action="/send_pygame" method="post">
                <input type="hidden" name="key" value="escape">
                <button class="menu-button" type="button">Main menu</button>
            </form>
            </div>
            `
        };
    }

    function renderState(nextState) {
        const views = getViews();
        if (!views[nextState]) return;
        if (nextState !== currentState) {
            waitAfterCountdown = false;
        }
        currentState = nextState;
        container.innerHTML = views[nextState];
        attachHoldHandlers();
    }

    renderState("main_menu");

    const socket = io();
    //This is here because I had a nightmare debugging the socketio stuff
    console.log('Connecting to Socket.IO...');

    // Listen for UI updates
    socket.on('update_ui', (data) => {
        console.log('Received update_ui:', data);
        if (data.state) {
            renderState(data.state);
        }
    });

    document.addEventListener('submit', async (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        if (!form.action.endsWith('/send_pygame') && !form.action.endsWith('/control_music')) return;

        event.preventDefault();
        console.log('submit handler fired for', form.action);
        const formData = new FormData(form);
        const key = formData.get("key");

        if (key === "p") {
            waitAfterCountdown = !waitAfterCountdown;
            renderState(currentState);
        }

        await fetch(form.action, {
            method: 'POST',
            body: formData
        });
    });

    function attachHoldHandlers() {
        const HOLD_MS = 2000;
        container.querySelectorAll('.menu-form').forEach(form => {
            const btn = form.querySelector('.menu-button');
            if (!btn) return;
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                console.log('native submit blocked for', form.action);
            }, {capture: true});
            const originalText = btn.textContent;
            let startTs = 0;
            let rafId = null;
            let activated = false;

            function updateCountdown() {
                if (!startTs) return;
                const elapsed = Date.now() - startTs;
                const remaining = Math.max(0, HOLD_MS - elapsed) / 1000;
                btn.textContent = `${originalText} (${remaining.toFixed(1)}s)`;
                if (elapsed < HOLD_MS) {
                    rafId = requestAnimationFrame(updateCountdown);
                }
            }

            function clearCountdown() {
                if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
                startTs = 0;
                btn.classList.remove('holding');
                btn.textContent = originalText;
                activated = false;
            }

            async function doActivate() {
                const formData = new FormData(form);
                console.log('hold complete, posting', form.action, Array.from(formData.entries()));
                const key = formData.get("key");
                if (key === "p") {
                    waitAfterCountdown = !waitAfterCountdown;
                    renderState(currentState);
                }
                try {
                            await fetch(form.action, { method: 'POST', body: formData });
                            try {
                                await fetch('/client_logs', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ logs: window._clientLogs || [], action: form.action, ts: Date.now() })
                                });
                            } catch (err) { console.warn('failed to send client logs', err); }
                } catch (err) {
                    console.error('activation fetch failed', err);
                }
            }

            function onPointerDown(e) {
                try { e.preventDefault(); } catch (err) {}
                console.log('pointer/touch down for', originalText);
                if (startTs) return;
                startTs = Date.now();
                btn.classList.add('holding');
                activated = false;
                rafId = requestAnimationFrame(updateCountdown);
            }

            function onPointerUp(e) {
                try { e.preventDefault(); } catch (err) {}
                console.log('pointer/touch up for', originalText);
                if (!startTs) return;
                const elapsed = Date.now() - startTs;
                if (elapsed >= HOLD_MS) {
                    activated = true;
                    doActivate();
                }
                clearCountdown();
            }

            btn.addEventListener('touchstart', onPointerDown, {passive: false});
            btn.addEventListener('touchend', onPointerUp);
            btn.addEventListener('pointerdown', onPointerDown, {passive: false});
            btn.addEventListener('pointerup', onPointerUp);
            btn.addEventListener('pointercancel', onPointerUp);
            btn.addEventListener('mouseleave', onPointerUp);

            btn.addEventListener('click', (e) => {
                if (!activated) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    clearCountdown();
                }
            }, {capture: true});
        });
    }
});
