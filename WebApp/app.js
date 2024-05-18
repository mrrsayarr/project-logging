
// Node.js 
const express = require('express');
const routes = require('./routes/route');
const path = require('path');

const app = express();
const port = 3000;

app.use('/', routes);

//app.use('eventlog', routes);
app.use(express.static('public'));

app.set("view engine", "ejs"); // Defining the image engine
app.set("views", path.join(__dirname, "views")); // Specifying the folder where the images will be located

app.use("/public", express.static(path.join(__dirname, "public"))); // Accessing the Public folder (this process is called mapping)


app.listen(port, () => {
  console.log(`Uygulama http://localhost:${port} adresinde çalışıyor`);
});