
// Node.js 
const express = require('express');
const routes = require('./routes/route');
const path = require('path');

const app = express();
const port = 3000;
const db = require('./db'); // Import the database module

// db.checkDbConnection(); // Checks the db connection

app.use('/', routes);

//app.use('eventlog', routes);
app.use(express.static('public'));

app.set("view engine", "ejs"); // Defining the image engine
app.set("views", path.join(__dirname, "views")); // Specifying the folder where the images will be located

app.use("/public", express.static(path.join(__dirname, "public"))); // Accessing the Public folder (this process is called mapping)

app.get('/eventlog', function(req, res) {
  db.readDataFromTable('events', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('eventlog', { events: data }); // 'events' değişkeni burada tanımlanır
      }
  });
});

app.get('/network', function(req, res) {
  db.readDataFromAnotherTable('IpLogs', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('network', { IpLogs: data }); // 'IpLogs' değişkeni burada tanımlanır
      }
  });
});

// app.get('/network', function(req, res) {
//   res.render('network');
// });


app.listen(port, () => {
  console.log(`Uygulama http://localhost:${port} adresinde çalışıyor`);
});