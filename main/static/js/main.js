// custom jQuery functions

// Get text only for selected element (not children notes)
$.fn.immediateText = function() {
    return this.contents().not(this.children()).text();
};
