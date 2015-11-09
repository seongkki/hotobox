/*
Author: Kyu & Moon
Modified from Googles Visualization
Purpose: Dust Chart 
*/

var spreadsheetURL = 'https://docs.google.com/spreadsheets/d/1NSEbUWojJsMzhH0hi8kx8ic7Xxuq29z0c7BXs-inzb8/edit#gid=0';
google.load("visualization", '1', {packages:['corechart']});
google.setOnLoadCallback(drawChart);

function drawChart() {
	var query = new google.visualization.Query(spreadsheetURL);
	$.getJSON("https://spreadsheets.google.com/feeds/list/1NSEbUWojJsMzhH0hi8kx8ic7Xxuq29z0c7BXs-inzb8/od6/public/basic?hl=en_US&alt=json", function(data) {
	colLen = data.feed.entry.length;
	
	var limit = 6;
	var offset = colLen - limit;
	
	queryOption = "limit "+limit+" offset "+offset;

 	query.setQuery(queryOption);
  	query.send(handleQueryResponse);
	});
}

function handleQueryResponse(response) {
	if (response.isError()) {
		alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
		return;
	}

	var data = response.getDataTable();
	var chart = new google.visualization.LineChart(document.getElementById('dailyChart'));
	var options = {
		width: 1100, height: 540,
		legend: 'none',
		pointSize: 5
      	};
  	chart.draw(data, options);
}
