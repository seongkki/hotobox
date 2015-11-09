var http = require("http"),
    url = require("url"),
    path = require("path"),
    fs = require("fs"),
	port = process.argv[2] || 10107;

var sys = require('sys');
var     exec = require('child_process').exec;
var     child;

pid=3690;

var IPAddress;
var gpio = require("pi-gpio");
var connect = require('connect');
var serveStatic = require('serve-static');
var os=require('os');
var ifaces=os.networkInterfaces();


for (var dev in ifaces) {
        ifaces[dev].forEach(function(details){
                if (details.family=='IPv4') {
                        if (details.address!="127.0.0.1"){
                }
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
			
				if (fs.statSync(filename).isDirectory()) filename += 'button.html';

				fs.readFile(filename, "binary", function(err, file) {
					if(err) {
						response.writeHead(500, {"Content-Type": "text/plain"});
						response.write(err + "\n");
						response.end();
						return;
			}	

			 if( request.method == 'GET' ) {
                id = request.url.substring(request.url.search("cmd=")+4,request.url.length);
                if (id=="ON") {
                        child=exec('sudo kill -s SIGBUS '+pid, function(error, stdout, sterr) {});
                        console.log('sent signal');
                //      LightOn();^M
                        }
                if (id=="OFF") {
                        console.log('off clicked');
                //      LightOff();^M
                        }
                response.writeHead(200);
                response.write("<script type='text/javascript'>location.href = 'http://68.232.126.94:10107/button.html'</script>");
                response.end();
                }
																        
		   });
		 });

	}	).listen(parseInt(port, 10));


console.log("Static file server running at\n  => http://localhost:" + port + "/\nCTRL + C to shutdown");


