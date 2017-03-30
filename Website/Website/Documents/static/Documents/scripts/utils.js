function postForAutoCompleteSearch(id_document_type) {
	$.ajax({
			url : "#",
			type : "POST",
			data : $(id_document_type).serialize(),
			success : function(document_type_data) {
				autoComplete(document_type_data);
			}
	});
};

function postForSearch(form, data_table_parent) {
	$.ajax({
			url : "#",
			type : "POST",
			data : $(form).serialize(),
			success : function(search_result) {
				if (search_result == "Not found") {
					showNotFound(data_table_parent);
				} else {
					var attribute_array = arrangeAttribute(data_table_parent);
					addData(search_result, attribute_array, data_table_parent);
				}
			}
	});
};

function getForDocument(asset_id_dict, data_table_parent) {
	$.ajax({
			url : "#",
			type : "GET",
			data : asset_id_dict,
			success : function(document_data) {
				var attribute_array = arrangeAttribute(data_table_parent);
				addData(document_data, attribute_array, data_table_parent, asset_id_dict);
			}
	});
};

function getForAsset(id_approval_agency, id_asset_type) {
	$.ajax({
		url : "#",
		type : "GET",
		data : $(id_approval_agency).serialize(),
		success : function(approval_agency_data) {
			changeAssetTypeSelection(id_approval_agency, id_asset_type, approval_agency_data);
		}
    });
};

function changeAssetTypeSelection(id_approval_agency, id_asset_type, approval_agency_data) {
	$(id_asset_type).empty();
	for(key in approval_agency_data) {
		item = approval_agency_data[key];
		$(id_asset_type).append($('<option>', {value: item['id'], text: item['asset_type']}));
	}
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
		new_row.innerHTML = "<td colspan='10' style='padding:0px'><div class='accordian-body collapse in' id = '" + id_dict['asset_id'] + "'><table class='table'><thead><tr><th>Actions</th><th>#</th><th>Document_type</th><th>Document_date</th><th>Renewal_date</th><th>A_number</th><th>License_decal_number</th><th>Model_number</th><th>Document_description</th></tr></thead><tbody></tbody></table></div></td>";
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
			console.log(item);
            if (data_table_parent == "asset_table_parent") {
				newRows += '<tr><th><span class="glyphicon glyphicon-pencil edit-asset"></span></th>';
			}
			else if(data_table_parent.nodeName == "TD" || data_table_parent == "document_table_parent"){
				newRows += '<tr><th><span class="glyphicon glyphicon-pencil edit-document"></span></th>';
			}
			else if(data_table_parent == "asset_table_in_document_parent") {
				newRows += '<tr draggable="true" ondragstart="rowDrag(event)">';
			}
			for (var i = 0; i < attribute_array.length; i++) {
				var attribute = attribute_array[i];
				if (item.hasOwnProperty(attribute)) { 
					if (data_table_parent == "asset_table_parent" && attribute == "id") {
						newRows += "<td>" + "<a href='#' id='asset_id'>" + item[attribute] + "</a></td>";
					} else {
						if(item[attribute] != null) {
						    newRows += "<td>" + item[attribute] + "</td>";
						}
					}
				}
			}
			if(data_table_parent == "asset_link_table_parent") {
				newRows += "<td><input type='button' class='btn btn-danger btn-xs' value='Delete'></td>";
			}
			newRows += "</tr>";
		}
		//console.log(newRows);
		//console.log(currentTable);
		currentTable.tBodies[0].innerHTML = newRows;
	}
};

function showNotFound(data_table_parent) {
	document.getElementById(data_table_parent).style.display = "none";
	document.getElementById("not_found").style.display = "block";
};

function arrangeAttribute(data_table_parent) {
	if(data_table_parent == 'asset_table_parent') {
		return ['id','approval_agency', 'asset_type', 'manufacture_name', 'serial_number', 'tag_number', 'status'];
	}
	else if(data_table_parent == 'asset_table_in_document_parent' || data_table_parent == 'asset_link_table_parent') {
		return ['id', 'approval_agency', 'serial_number', 'tag_number', 'status'];
	}
	else {
		return ['id','document_type', 'document_date', 'renewal_date', 'a_number', 'license_decal_number', 'model_number', 'document_description'];
	}
}

function autoComplete(document_type_data) {
	var document_type_attributes = [];
	for (key in document_type_data) {
		if (document_type_data.hasOwnProperty(key)) {
			var item = document_type_data[key];
			document_type_attributes.push({
				label : item['document_type'],
				real_id : item['id']
			});
		}
	}
	$('#id_document_type').autocomplete(
		{
			source : document_type_attributes,
			select : function(e, ui) {
				document.getElementById("document_type_id").value = ui.item.real_id;
		},
	});
}

function checkAssetIdBeforeSubmit() {
	var valueArray = [];
	$('#asset_selected_table > tbody  > tr').each(function() {
		valueArray.push($(this).find('td:first').text());
	});
	if(valueArray.length == 0) {
		$('.alert').show();
		$('.alert').attr('class', 'alert alert-danger');
		$('.alert').css('font-weight', 'bold');
		return false;
	}
	document.getElementById('asset_id').value = valueArray;	
};

function allowDrop(event) {
	event.preventDefault();
}

function rowDrag(event) {
	event.dataTransfer.setData("html", event.target.innerHTML);
}

function drop(event) {
	event.preventDefault();
	$('.alert').hide();
	var row_data = document.createElement('tr');
	row_data.innerHTML = event.dataTransfer.getData("html")
			+ "<td><input type='button' class='btn btn-danger btn-xs' value='Delete'></td>";
	$('#asset_selected_table > tbody').append(row_data);
	var asset_id = $(row_data).find('td:first').text();
}

$(function() {
	$('#id_document_date, #id_renewal_date').datepicker({
		dateFormat : "yy-mm-dd"
	});
});

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
