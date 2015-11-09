/*
Author: Kyu & Moon
Modified Googles Visualization
Purpose: Humidity Chart 
*/

var spreadsheetURL = 'https://docs.google.com/spreadsheets/d/1WSiG5bsxeoXqCJboMLEvf0Scusg9Y_ZvY-H1fFTIOL4/edit#gid=0';
google.load("visualization", '1', {packages:['corechart']});
google.setOnLoadCallback(drawChart);

function drawChart() {
	var query = new google.visualization.Query(spreadsheetURL);
	$.getJSON("https://spreadsheets.google.com/feeds/list/1WSiG5bsxeoXqCJboMLEvf0Scusg9Y_ZvY-H1fFTIOL4/od6/public/basic?hl=en_US&alt=json", function(data) {

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
		width: 1200, height: 540,
		legend: 'none',
		pointSize: 5
      	};
				title: "Temperature Daily Status",
  	chart.draw(data, options);
}
