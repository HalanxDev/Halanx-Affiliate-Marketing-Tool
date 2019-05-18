(function() {

    // Localize jQuery variable
    let jQuery;

    /******** Load jQuery if not present *********/
    if (window.jQuery === undefined || window.jQuery.fn.jquery !== '3.4.0') {
        let script_tag = document.createElement('script');
        script_tag.setAttribute("type","text/javascript");
        script_tag.setAttribute("src",
            "https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js");
        if (script_tag.readyState) {
          script_tag.onreadystatechange = function () { // For old versions of IE
              if (this.readyState === 'complete' || this.readyState === 'loaded') {
                  scriptLoadHandler();
              }
          };
        } else { // Other browsers
          script_tag.onload = scriptLoadHandler;
        }
        // Try to find the head, otherwise default to the documentElement
        (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
    } else {
        // The jQuery version on the window is the one we want to use
        jQuery = window.jQuery;
        main();
    }

	/******** Called once jQuery has loaded ******/
	function scriptLoadHandler() {
		// Restore $ and window.jQuery to their previous values and store the
		// new jQuery in our local jQuery variable
		jQuery = window.jQuery.noConflict(true);
		// Call our main function
		main();
	}

	/******** Our main function ********/
	function main() {
		jQuery(document).ready(function($) {
            /******* Load CSS *******/
            let css_link = $("<link>", {
                rel: "stylesheet",
                type: "text/css",
                href: "http://127.0.0.1:8000/static/widgets/css/style.css"
            });
            css_link.appendTo('head');

            /******* Load HTML *******/
            let widget_url = "http://127.0.0.1:8000/widgets/data.js?callback=?";
            $.getJSON(widget_url, function(data) {
                $('#widget-container').html(data.html);
            });
		});
	}

})();