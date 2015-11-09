//variables for http serving
var 	http = require("http").createServer(handler),
    	url = require("url"),
    	path = require("path"),
    	fs = require("fs"),
	port = process.argv[2] || 10110;
http.listen(parseInt(port, 10));
//variables for sending signals
var 	sys = require('sys'),
	exec = require('child_process').exec,
	child,
	pid=3690;

var connect = require('connect');
var serveStatic = require('serve-static');
var os=require('os');
var ifaces=os.networkInterfaces();


var sen_File = "inter.json";
var sen_File2 = "counter.json";
var rel_File = "rel_int.json";
var rel_File2 = "rel_on.json";
var io = require('socket.io').listen(http);

//save web updated JSON to file
function save_json (data, jsonFile) {

	fs.writeFile(jsonFile, JSON.stringify(JSON.parse(data), null, 4), function(err) { if(err) {
		console.log(err);
	} else {
		console.log("JSON saved to " + jsonFile);
	}
	});
}


//create http server
function handler(request, response) {

var uri = url.parse(request.url).pathname;
var filename = path.join(process.cwd(), uri);


		path.exists(filename, function(exists) {
			if(!exists) {
				response.writeHead(404, {"Content-Type": "text/plain"});
				response.write("404 Not Found\n");
				response.end();
				return;
			}
		
			
			if (fs.statSync(filename).isDirectory()) filename += 'main.html';
			
			fs.readFile(filename, "binary", function(err, file) {
				if(err) {
					response.writeHead(500, {"Content-Type": "text/plain"});
					response.write(err + "\n");
					response.end();
					return;

				}
				var o = "";
				if ( request.method == 'POST' ) {
					var store = '';
				
					console.log("received post request");
					
					
					request.on('/bb.html', function(data)
					{
						console.log("myaction");
					});

					request.on('data', function(data)
					{
						store += data;
						/*if(true)
						{
							console.log("sensorJSON");
							save_json(store, sen_File);
	                                                response.end(store);
						}
						else {
							console.log("relayJSON");
							save_json(store, rel_File);
							response.end(store);
						}*/
						
						o = JSON.parse(store);
					});
				
					request.on('end', function(sender)
					{
						
					//	console.log("end recived from"+o.interrupt.sender);
						if(o.interrupt.sender == 1)
						{
							console.log("relayJSON");
							save_json(store, rel_File);
	                                                response.end(store);
						}
						else {
							console.log("sensorJSON");
							save_json(store, sen_File);
							response.end(store);
						}
						response.end();
					});

				}
			response.writeHead(200);
			response.write(file, "binary");
			response.end();
			});
		});
}


			io.sockets.on('connection', function(socket) {
    				fs.watchFile(sen_File2, function (curr, prev) {
			        	console.log('the current mtime is: ' + curr.mtime);
			            	console.log('the previous mtime was: ' + prev.mtime);


				fs.readFile(sen_File2, function(err, data) {
			            	if (err) throw err;

				    	var data = JSON.parse(data);
				            socket.emit('notification', data);
				        });
				});
    				
				fs.watchFile(rel_File2, function (curr, prev) {
			        	console.log('the current mtime is: ' + curr.mtime);
			            	console.log('the previous mtime was: ' + prev.mtime);


				fs.readFile(rel_File2, function(err, data) {
			            	if (err) throw err;

				    	var data = JSON.parse(data);
				            socket.emit('notification', data);
				        });
			});
			});
	

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
