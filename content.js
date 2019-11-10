
//crossref["Genesis"][0].forEach( verseWriter );
var bookAndChapter = document.getElementsByClassName("passage-display-bcv")[0].innerHTML;
//alert(bookAndChapter);
chapter = crossref[bookAndChapter];
verseList = Object.keys(chapter);

// "in" here is not working as expected, it should return the elements in the array,
// instead its returning the positions of the elements
for (var i in verseList) {
		verse = verseList[i]
		//alert(verse);
  	verseWriter( chapter[verse], verse, chapter);
}
//class="passage-display-bcv"

function verseWriter(value, verse, array) {


  var span = document.getElementsByClassName(verse)[0];

  var img = document.createElement("span");
  img.innerHTML='<img src="'+chrome.extension.getURL("egw.png")+'" alt="[EGW]" class="egw_image" width="15" height="15" onClick="document.getElementById(\'egw_v'+verse+'\').style.display=\'inline\'">';
  span.appendChild(img);

  var egw = document.createElement("span");
  egw.className = "EGW";
  egw.id = "egw_v"+verse;
  egw.style.display="none";
  span.appendChild(egw);


  crossref[bookAndChapter][verse].forEach( indexWriter );
  function indexWriter(value, index, array) {
  	a = document.createElement("a");
  	a.title = value["name"];
  	a.href = "https://m.egwwritings.org/" + value["link"];
		a.className = "egwlink";
		a.style = 'color: rgb(21, 136, 177)';
  	var x = document.createTextNode(" " + value["name"]);
  	a.appendChild(x);
  	egw.appendChild(a);
  }
}

/*
Needed for modal dialog, but need to solve CORS issues first

addHTML(chrome.extension.getURL('modal.html'));

function createDiv(responsetext)
{
    var _body = document.getElementsByTagName('body')[0];
    var _div = document.createElement('div');
    _div.innerHTML = responsetext;
    _body.appendChild(_div);
}

function addHTML(theUrl)
{
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            createDiv(xmlhttp.responseText);
        }
    }
    xmlhttp.open("GET", theUrl, false);
    xmlhttp.send();
}

var s = document.createElement('script');
s.src = chrome.extension.getURL('modal.js');
(document.head||document.documentElement).appendChild(s);
*/

/* NOT NEEDED
s.onload = function() {
	s.parentNode.removeChild(s);
};
/* NOT NEEDED
var s = document.createElement('div');
s.innerHTML = chrome.extension.getURL('modal.html');
(document.body||document.documentElement).appendChild(s);
*/
