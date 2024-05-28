
// Node.js 
const express = require('express');
const routes = require('./routes/route');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// db.checkDbConnection(); // Checks the db connection

app.use(bodyParser.json()); // bodyParser.json() middleware'ini kullanarak gelen isteklerin JSON gövdelerini ayrıştırırız
app.use(bodyParser.urlencoded({ extended: true })); // URL kodlamalı gövdeleri ayrıştırmak için

app.use('/', routes);

//app.use('eventlog', routes);
app.use(express.static('public'));


app.set("view engine", "ejs"); // Defining the image engine
app.set("views", path.join(__dirname, "views")); // Specifying the folder where the images will be located

// app.set('views', path.join(__dirname, '../master')); // Python Scriptleri için
app.use("/public", express.static(path.join(__dirname, "public"))); // Accessing the Public folder (this process is called mapping)

app.use('/', routes); // route.js'deki router'ı kullanıyoruz


app.listen(port, () => {console.log(`Uygulama http://localhost:${port} adresinde çalışıyor`);});


