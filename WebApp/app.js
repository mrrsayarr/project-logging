
// Node.js 
const express = require('express');
const routes = require('./routes/route');
const path = require('path');
const db = require('./db'); // Import the database module
var bodyParser = require('body-parser');

const app = express();
const port = 3000;

// db.checkDbConnection(); // Checks the db connection

app.use('/', routes);

//app.use('eventlog', routes);
app.use(express.static('public'));

app.use(bodyParser.json()); // bodyParser.json() middleware'ini kullanarak gelen isteklerin JSON gövdelerini ayrıştırırız

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
  db.readDataFromTable('IpLogs', ['PID', 'Process', 'Protocol', 'StartTime', 'CommunicationProtocol', 'LocalIP', 'LocalPort', 'RemoteIP', 'RemotePort'], function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('network', { IpLogs: data }); // 'IpLogs' değişkeni burada tanımlanır
      }
  });
});

app.get('/news', function(req, res) {
  db.readDataFromTable('news', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('news', { news: data });
      }
  });
});

// app.get('/filewatcher', function(req, res) {
//   db.readDataFromTable('file_logs', function(err, data) {
//       if (err) {
//           console.error(err);
//           res.status(500).send('Server Error');
//       } else {
//           res.render('filewatcher', { file_logs: data });
//       }
//   });
// });

app.get('/filewatcher', function(req, res) {
  db.readDataFromTable('file_logs', function(err, file_logs) {
    if (err) {
      console.error(err);
      return res.status(500).send('Server Error');
    }

    db.readDataFromTable('watch_paths', function(err, watch_paths) {
      if (err) {
        console.error(err);
        return res.status(500).send('Server Error');
      }

      // Veritabanından path değerini al
      var path = watch_paths[0].path;
      // path değerini ve file_logs verisini ejs dosyasına gönder
      res.render('filewatcher', { path: path, file_logs: file_logs });
    });
  });
});

app.post('/update-path', function(req, res) {
  var newPath = req.body.newPath; // Kullanıcının girdiği yeni yolu alırız

  // Veritabanında yolu güncelleriz
  var tableName = 'watch_paths';
  var updates = `path = '${newPath}'`;
  var condition = 'id = 1'; // Burada, güncellenecek yolun ID'sini belirtiyoruz. Bu, sizin durumunuza bağlı olarak değişebilir.

  // db.js dosyasından gelen updateDataInTable fonksiyonunu kullanırız
  db.updateDataInTable(tableName, updates, condition, function(err) {
    if (err) {
      console.error(err);
      res.status(500).send('Server Error');
    } else {
      res.send('Yol başarıyla güncellendi');
    }
  });
});

// app.get('/filewatcher', function(req, res, next) {
//   res.render('filewatcher', { title: 'File Watcher' });
// });

// app.get('/news', function(req, res, next) {
//   res.render('news', { title: 'News', news: ['News 1', 'News 2', 'News 3'] });
// });

// app.get('/network', function(req, res) {
//   res.render('network');
// });


app.listen(port, () => {
  console.log(`Uygulama http://localhost:${port} adresinde çalışıyor`);
});