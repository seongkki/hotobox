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
var connect = require('connect');
var serveStatic = require('serve-static');
var os=require('os');
var ifaces=os.networkInterfaces();

//save web updated JSON to file
function save_json (data) {
	var outputFilename = 'sensorVar.json';

	fs.writeFile(outputFilename, JSON.stringify(JSON.parse(data), null, 4), function(err) { if(err) {
		console.log(err);
	} else {
		console.log("JSON saved to " + outputFilename);
	}
	});
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
//create http server
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

				if ( request.method == 'POST' ) {
					var store = '';
				
					console.log("received post request");

					request.on('data', function(data)
					{
						store += data;
						save_json(store);
						response.end(store);
					});
				
					request.on('end', function()
					{
						console.log("end function");
						response.end();
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
for (var dev in ifaces) {
	ifaces[dev].forEach(function(details){
		if (details.family=='IPv4') {
			if (details.address!="127.0.0.1"){
		}
	  }
	});
}

*/
