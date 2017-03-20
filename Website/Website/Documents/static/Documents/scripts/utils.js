
function postForHintSearch(){
	$.ajax({
		url : "#", 
		type : "POST", 
		data : $('#id_document_type').serialize(),
        success : function(json) {       	 
        	console.log("hintsearchSuccess");
        	addHint(json);
        },
        error : function(xhr,erråmsg,err) {
           $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
           " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function postForSearch(form, table) {
	
	$.ajax({
		url : "#", 
		type : "POST", 
		data : $(form).serialize(),
        success : function(json) {       	 
        	if(json == "Not found") {
        		showNotFound(table);
        	}
        	else{
        		sortedKey = sortData(json[0]);
                addData(json, sortedKey, table);
            }
        },

        error : function(xhr,erråmsg,err) {
           $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
           " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
 * The functions below will create a header with csrftoken
 */

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e
		// relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function addData(result, sortedKey, table) {
	var currentTable = document.getElementById(table);
	console.log(currentTable.id);
	currentTable.style.display="table";
	document.getElementById("not_found").style.display="none";
	var newRows = " ";
	for(key in result) {
		if(result.hasOwnProperty(key)){
			var item = result[key];		
	        newRows += "<tr>";
	        if(currentTable.id == "asset_table_in_search" || currentTable.id == "document_table") {
	            newRows +=  '<th><span class="glyphicon glyphicon-pencil edit-document"></span></th>';
	        }
	        for(var i = 0; i < sortedKey.length; i++){
	        	var attribute = sortedKey[i];
	    	    if(item.hasOwnProperty(attribute)) {
	    	            newRows += "<td align='center'>" + item[attribute] + "</td>";
	    	    }
	        }
	        newRows += "</tr>";
		}
	    currentTable.tBodies[0].innerHTML = newRows;
	}
};

function showNotFound(table) {
	document.getElementById(table).style.display="none";
	document.getElementById("not_found").style.display="block";
};

function sortData(item) {
	var keyArray = [];
	for(key in item) {
		if(item.hasOwnProperty(key) && key != 'asset_type_id' && key != 'approval_agency_id' && key != 'document_type_id' && key != 'description' && key != 'id') {
			keyArray.push(key);
		}
	}
	keyArray.sort();
	if('approval_agency' in item) {
		keyArray.push('description');
	}
    keyArray.unshift('id');
    console.log(keyArray);
	return keyArray;
}

function addHint(result) {
	var document_type_attributes = [];
	for(key in result) {
		if(result.hasOwnProperty(key)){
			var item = result[key];	
			document_type_attributes.push({label : item['document_type'], real_id : item['id']});
		}
	}
	console.log(document_type_attributes);
	$('#id_document_type').autocomplete({ 
		source : document_type_attributes,
		select: function(e, ui) {
			document.getElementById("document_type_id").value = ui.item.real_id;
		},
	});
}

