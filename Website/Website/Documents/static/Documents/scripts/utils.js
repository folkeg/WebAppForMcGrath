function post(dataType) {
	
	$.ajax({
		url : "#", // the endpoint
		type : "POST", // http method
		data : (dataType == asset_data) ? $('#asset_data').serialize() : $('#document_data').serialize(),
		// handle a successful response
        success : function(json) {       	 
        	if(json == "Not found") {
        		showNotFound();
        	}
        	else{
        		sortedKey = sortData(json[0]);
                addData(json, sortedKey);
            }
        },

        // handle a non-successful response
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


function addData(result, sortedKey) {
	document.getElementById("asset_table").style.display="table";
	var newRows = " ";
	for(key in result) {
		if(result.hasOwnProperty(key)){
			var item = result[key];		
	        newRows += "<tr><th>";
	        newRows +=  '<span class="glyphicon glyphicon-pencil edit-document"></span>';
	        newRows += "</th>";
	        for(var i = 0; i < sortedKey.length; i++){
	        	var attribute = sortedKey[i];
	    	    if(item.hasOwnProperty(attribute)) {
	    	        newRows += "<td align='center'>" + item[attribute] + "</td>";
	    	    }
	        }
	        newRows += "</tr>";
		}
	    document.getElementById("asset_row").innerHTML = newRows;
	}
};

function showNotFound() {
	document.getElementById("asset_table").style.display="none";
	document.getElementById("document_table").style.display="none";
	var content = "<p>No result found.</p>"
	document.getElementById("not_found").innerHTML = content;
};

function sortData(item) {
	var keyArray = [];
	for(key in item) {
		if(item.hasOwnProperty(key) && key != 'asset_type_id' && key != 'approval_agency_id' && key != 'document_type_id' && key != 'search_type' &&key != 'description' && key != 'id') {
			keyArray.push(key);
		}
	}
    keyArray.sort();
    keyArray.push('description');
    keyArray.unshift('id');
    console.log(keyArray);
	return keyArray;
}

