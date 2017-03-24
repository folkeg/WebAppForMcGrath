function postForAutoCompleteSearch() {
	$.ajax({
			url : "#",
			type : "POST",
			data : $('#id_document_type').serialize(),
			success : function(json) {
				autoComplete(json);
			}
	});
};

function postForSearch(form, data_table_parent) {
	$.ajax({
			url : "#",
			type : "POST",
			data : $(form).serialize(),
			success : function(json) {
				if (json == "Not found") {
					showNotFound(data_table_parent);
				} else {
					var attribute_array = arrangeAttribute(json[0]);
					addData(json, attribute_array, data_table_parent);
				}
			}
	});
};

function getForDocument(data, data_table_parent) {
	$.ajax({
			url : "#",
			type : "GET",
			data : data,
			success : function(json) {
				var arranged_attribute_name = arrangeAttribute(json[0]);
				addData(json, arranged_attribute_name, data_table_parent, data);
			}
	});
};

function getForAssetEdit(data) {
	$.ajax({
		url : "#",
		type : "GET",
		data : data,
		success : function(json) {
			var arranged_attribute_name = arrangeAttribute(json[0]);
			addData(json, arranged_attribute_name, data_table_parent, data);
		}
    });
};

function ajaxResponseError(xhr, erråmsg, err) {
	$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "
		                + errmsg
			            + " <a href='#' class='close'>&times;</a></div>"); 	
	console.log(xhr.status + ": " + xhr.responseText); 
};


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie
						.substring(name.length + 1));
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
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/')
			|| (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin
					+ '/') ||
			// or any other URL that isn't scheme relative or absolute i.e
			// relative.
			!(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
	beforeSend : function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
			// Send the token to same-origin, relative URLs only.
			// Send the token only if the method warrants CSRF protection
			// Using the CSRFToken value acquired earlier
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function addData(result, attribute_array, data_table_parent, id_dict) {
	var currentTable = "";
	if (data_table_parent.nodeName == "TD") {
		$(data_table_parent).addClass("accordion-toggle");
		$(data_table_parent).attr("data-toggle", "collapse");
		$(data_table_parent).attr("data-target", '#' + id_dict['asset_id']);
		var new_row = document.createElement('tr');
		$(new_row).attr("id", "tr_table");
		new_row.innerHTML = "<td colspan='10' style='padding:0px'><div class='accordian-body collapse in' id = '" + id_dict['asset_id'] + "'><table class='table'><thead><tr><th>Actions</th><th>#</th><th>Document_type</th><th>Document_date</th><th>Renewal_date</th><th>Manufacture_name</th><th>A_number</th><th>License_decal_number</th><th>Model_number</th><th>Document_description</th></tr></thead><tbody></tbody></table></div></td>";
		data_table_parent.parentElement.after(new_row);
		currentTable = $(new_row).find('table')[0];
	}
	else{
		document.getElementById(data_table_parent).style.display = "block";
		currentTable = document.getElementById(data_table_parent).getElementsByTagName("table")[0];
		document.getElementById("not_found").style.display = "none";
	}
	var newRows = " ";
	for (key in result) {
		if (result.hasOwnProperty(key)) {
			var item = result[key];
			newRows += "<tr>";
			if (data_table_parent == "asset_table_parent") {
				newRows += '<th><span class="glyphicon glyphicon-pencil edit-asset"></span></th>';
			}
			else if (data_table_parent == "document_table_parent") {
				newRows += '<th><span class="glyphicon glyphicon-pencil edit-document"></span></th>';
			}
			for (var i = 0; i < attribute_array.length; i++) {
				var attribute = attribute_array[i];
				if (item.hasOwnProperty(attribute)) {
					if (data_table_parent == "asset_table_parent" && attribute == "id") {
						newRows += "<td>" + "<a href='#' id='asset_id'>" + item[attribute] + "</a></td>";
					} else {
						console.log("here");
						if(item[attribute] != null) {
						    newRows += "<td>" + item[attribute] + "</td>";
						}
					}
				}
			}
			newRows += "</tr>";
		}
		currentTable.tBodies[0].innerHTML = newRows;
	}
};

function showNotFound(data_table_parent) {
	document.getElementById(data_table_parent).style.display = "none";
	document.getElementById("not_found").style.display = "block";
};

function arrangeAttribute(item) {
	if('approval_agency' in item) {
		return ['id','approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status'];
	}
	else {
		return ['id','document_type', 'document_date', 'renewal_date', 'a_number', 'license_decal_number', 'model_number', 'document_description'];
	}
}

function autoComplete(result) {
	var document_type_attributes = [];
	for (key in result) {
		if (result.hasOwnProperty(key)) {
			var item = result[key];
			document_type_attributes.push({
				label : item['document_type'],
				real_id : item['id']
			});
		}
	}
	console.log(document_type_attributes);
	$('#id_document_type').autocomplete(
		{
			source : document_type_attributes,
			select : function(e, ui) {
				document.getElementById("document_type_id").value = ui.item.real_id;
		},
	});
}

function exportTableToCSV($table, filename) {
	var $headers = $table.find('tr:has(th)');
	var $rows = $table.children('tr').not('tr > tr');

	// Temporary delimiter characters unlikely to be typed by keyboard
	// This is to avoid accidentally splitting the actual contents
	var tmpColDelim = String.fromCharCode(11); // vertical tab character
	var tmpRowDelim = String.fromCharCode(0) // null character

	// actual delimiter characters for CSV format
	var colDelim = '","'
	var rowDelim = '"\r\n"';

	// Grab text from table into CSV formatted string
	var csv = '"';
	csv += formatRows($headers.map(grabRow));
	csv += rowDelim;
	csv += formatRows($rows.map(grabRow)) + '"';

	// Data URI
	var csvData = 'data:application/csv;charset=utf-8,'
			+ encodeURIComponent(csv);

	// For IE (tested 10+)
	if (window.navigator.msSaveOrOpenBlob) {
		var blob = new Blob([ decodeURIComponent(encodeURI(csv)) ], {
			type : "text/csv;charset=utf-8;"
		});
		navigator.msSaveBlob(blob, filename);
	} else {
		$(this).attr({
			'download' : filename,
			'href' : csvData
		// ,'target' : '_blank' //if you want it to open in a new window
		});
	}

	// Format the output so it has the appropriate delimiters
	function formatRows(rows) {
		return rows.get().join(tmpRowDelim).split(tmpRowDelim).join(rowDelim)
				.split(tmpColDelim).join(colDelim);
	}
	// Grab and format a row from the table
	function grabRow(i, row) {

		var $row = $(row).not('#tr_table');
		// for some reason $cols = $row.find('td') || $row.find('th') won't
		// work...
		var $cols = $row.find('td');
		if (!$cols.length)
			$cols = $row.find('th').not(':first');

		return $cols.map(grabCol).get().join(tmpColDelim);
	}
	// Grab and format a column from the table
	function grabCol(j, col) {
		var $col = $(col);
		var $text = $col.text();

		return $text.replace('"', '""'); // escape double quotes

	}
}
