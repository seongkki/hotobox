//variables for http serving
var 	http = require("http"),
    	url = require("url"),
    	path = require("path"),
    	fs = require("fs"),
	port = process.argv[2] || 10110;

//variables for sending signals
var 	sys = require('sys'),
	exec = require('child_process').exec,
	child,
	pid=3690;

var IPAddress;
var gpio = require("pi-gpio");
var connect = require('connect');
var serveStatic = require('serve-static');
var os=require('os');
var ifaces=os.networkInterfaces();

//save web updated JSON to file
function save_json (data) {
	var outputFilename = 'sensorVar.json';

	fs.writeFile(outputFilename, JSON.stringify(data, null, 4), function(err) {
	if(err) {
		console.log(err);
	} else {
		console.log("JSON saved to " + outputFilename);
	}
	});
}

http.createServer(function(request, response) {

var uri = url.parse(request.url).pathname;
var filename = path.join(process.cwd(), uri);


		path.exists(filename, function(exists) {
			if(!exists) {
				response.writeHead(404, {"Content-Type": "text/plain"});
				response.write("404 Not Found\n");
				response.end();
				return;
			}
		
				if (fs.statSync(filename).isDirectory()) filename += 'bb.html';
			
				fs.readFile(filename, "binary", function(err, file) {
					if(err) {
						response.writeHead(500, {"Content-Type": "text/plain"});
						response.write(err + "\n");
						response.end();
						return;

					}

			if( request.method == 'GET' ) {
                		id = request.url.substring(request.url.search("cmd=")+4,request.url.length);
		                if (id=="TEMP") {	
		                        child=exec('sudo kill -s SIGBUS '+pid, function(error, stdout, sterr) {});
        		                console.log('temp signal');
                		//      LightOn();
                        	}
	              		else if (id=="HUMID") {
        	                	console.log('humid signal');
	        	        //      LightOff();
                        	}
				else if (id=="DUST") {
					console.log('dust signal');
				}
			}	
			if ( request.method == 'POST' ) {
				var store = '';
				
				console.log("received post request");

				request.on('data', function(data)
				{
					store += data;
				});
				
				request.on('end', function()
				{
					save_json(store);
					response.setHeader("Content-Type", "text/json");
				        response.setHeader("Access-Control-Allow-Origin", "*");
				        response.end(store);
				});

			}
			
			response.writeHead(200);
			response.write(file, "binary");
			response.end();
			});
		});

	}).listen(parseInt(port, 10));

console.log("Static file server running at\n  => http://localhost:" + port + "/\nCTRL + C to shutdown");

/*
function LightOn() {
	gpio.open(18, "output", function(err) {
		gpio.write(18, 1, function() {
			gpio.close(18);
		});
	});
}

function LightOff() {
	gpio.open(12, "output", function(err) {
		gpio.write(12, 0, function() {
			gpio.close(12);
		});
	});
}
*/
/*
for (var dev in ifaces) {
	ifaces[dev].forEach(function(details){
		if (details.family=='IPv4') {
			if (details.address!="127.0.0.1"){
		}
	  }
	});
}

*/
