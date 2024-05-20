if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    scroll_to_text: function(n_clicks) {
        if (n_clicks > 0) {
            setTimeout(function() {
                document.getElementById('additional-content').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 200); // A slight delay to ensure the DOM has updated
        }
        return ''; // Prevent updating any Output
    },
    scroll_to_map: function(selected_trail) {
        if(selected_trail) {
            setTimeout(function() {
                document.getElementById('mytrail-map').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100); // A slight delay to ensure the DOM has updated
        }
        return window.dash_clientside.no_update; // Prevent updating any Output
    },
};
