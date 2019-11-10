/*
document.getElementById('button').addEventListener("click", function() {
	document.querySelector('.egw-modal').style.display = "flex";
});
*/

var linkElements = document.getElementsByClassName('egwlink');
Array.prototype.forEach.call(linkElements, function(link) {
	link.addEventListener("click", egwClickHandler );
});

document.querySelector('#egw-modal-close').addEventListener("click", function() {
	document.querySelector('.egw-modal').style.display = "none";
});

//alert("gothere");

//var egwClickHandler = function (e) {

var isNewTab = function (e) {
		return e.ctrlKey || e.shiftKey || e.metaKey || (e.button && e.button === 1);
};

function egwClickHandler(e) {

		//alert("in click Handler");
    if (isNewTab(e)) {
        return;
    }

    var $me = $(e.currentTarget), i;

    if ($me.hasClass('egwlink')) {
        e.preventDefault();
        self.showReference($me);
        return;
    }

    return;
};

this.showReference = function ($link) {
    var href = $link[0].href;
    $.ajax({
        type: "POST",
        url: href,
        dataType: 'html',
        data: {type: 'chunk'},
        success: function (html) {
            var $content = $(html);
            var $dialog = $('#egw-link-dialog');
            $dialog.find('.modal-title').text($link.text());
            $dialog.find('.modal-body').html($content.find('.egw_content_container'));
            $dialog.find('.egw-link-dialog-href').attr('href', href);
            $dialog.modal();
        }/*,
        error: function () {
            handleError(href);
        }*/
    });
};
