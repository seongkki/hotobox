var express = require("express");
var app = express();

app.set('views', __dirname + '/public/views');
app.set('view engine', 'html');

/* serves main page */
app.get("/", function(req, res) {
	      res.sendfile('button.html')
});

app.post('/test', function (req, res) {
	    console.log('works!!');
});

// catch 404 and forwarding to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
        err.status = 404;
            next(err);
});


/* serves all the static files */
app.get(/^(.+)$/, function(req, res){ 
	      console.log('static file request : ' + req.params);
		       res.sendfile( __dirname + req.params[0]); 
			    });

var port = process.env.PORT || 10107;
  	app.listen(port, function() {
  	console.log("Listening on " + port);
});
