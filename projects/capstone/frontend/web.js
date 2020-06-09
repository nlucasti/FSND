// var gzippo = require('gzippo');
// var express = require('express');
// var morgan = require('morgan');
// var app = express();
//
// app.use(morgan('dev'));
// app.use(gzippo.staticGzip("" + __dirname + "/www"));
//
// app.get('*', function(req,res) {
//
// res.sendFile(path.join(__dirname+'/www/index.html'));
// console.log('running')
// });
//
// app.listen(process.env.PORT || 8080);

// 404 catch
const express = require('express');
const http = require('http')
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, '/www')));

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authotization");
  next();
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname + '/www/index.html'));
});

const port = process.env.PORT || 3000;
app.set('port', port);

const server = http.createServer(app);
server.listen(port, () => console.log('running'))
