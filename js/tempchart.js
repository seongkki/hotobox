var spreadsheetURL = 'https://docs.google.com/spreadsheets/d/1d_HO7QIpyATO9Ut7rQ0Iwr0vmaYYPZ82LniCD9X5Nsc/edit#gid=0';
google.load("visualization", '1', {packages:['corechart']});
google.setOnLoadCallback(drawChart);

function drawChart() {
	var query = new google.visualization.Query(spreadsheetURL);
	$.getJSON("https://spreadsheets.google.com/feeds/list/1d_HO7QIpyATO9Ut7rQ0Iwr0vmaYYPZ82LniCD9X5Nsc/od6/public/basic?hl=en_US&alt=json", function(data) {
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
		width: 1300, height: 600,
		legend: 'none',
		pointSize: 5
      	};
	title: "Temperature Daily Status",
  	chart.draw(data, options);
}
