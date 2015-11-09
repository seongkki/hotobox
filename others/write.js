var port = 10109;
var http = require("http");
var server = http.createServer();
var fs = require("fs");
server.on('request', request);
server.listen(port);

function save_json(data) {
        var outputFilename = 'sensor.json';
	
        fs.writeFile(outputFilename, JSON.stringify(JSON.parse(data), null, '\t'), function(err) {
        	if(err) {
                	console.log(err);
	        } else {
        	        console.log("JSON saved to " + outputFilename);
	        }
        });
}

function request(request, response) {
    var store = '';

    request.on('data', function(data) 
    {
        store += data;
    });
    request.on('end', function() 
    { 	
	//console.log(store);
        response.setHeader("Content-Type", "text/json");
        response.setHeader("Access-Control-Allow-Origin", "*");
	save_json(store); 
        response.end(store)
    });
 }  
