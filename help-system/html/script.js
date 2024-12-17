window.addEventListener('message', function(event) {
    if (event.data.type === "help") {
        document.getElementById('help-menu').style.display = event.data.display ? 'block' : 'none';
    } else if (event.data.type === "admin") {
        document.getElementById('admin-menu').style.display = event.data.display ? 'block' : 'none';
    }
});

document.onkeyup = function(event) {
    if (event.key === 'Escape') {
        fetch(`https://${GetParentResourceName()}/closeMenu`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
    }
};
