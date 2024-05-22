
var express = require('express');
var router = express.Router();
var db = require('../db');

// Rotalarınızı burada tanımlayın
router.get('/', function(req, res) {
  res.render('index');
});

router.get('/eventlog', function(req, res) {
  db.readDataFromTable('events', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('eventlog', { events: data }); // 'events' değişkeni burada tanımlanır
      }
  });
});

// router.get('/network', function(req, res) {
//   db.readDataFromTable('IpLogs', ['PID', 'Process', 'Protocol', 'StartTime', 'CommunicationProtocol', 'LocalIP', 'LocalPort', 'RemoteIP', 'RemotePort'], function(err, data) {
//       if (err) {
//           console.error(err);
//           res.status(500).send('Server Error');
//       } else {
//           res.render('network', { IpLogs: data }); // 'IpLogs' değişkeni burada tanımlanır
//       }
//   });
// });

router.get('/network', function(req, res) {
  db.readDataFromTable('IpLogs', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('network', { IpLogs: data }); // 'IpLogs' değişkeni burada tanımlanır
      }
  });
});

router.get('/news', function(req, res) {
  db.readDataFromTable('news', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('news', { news: data });
      }
  });
});

// router.get('/filewatcher', function(req, res) {
//   db.readDataFromTable('file_logs', function(err, data) {
//       if (err) {
//           console.error(err);
//           res.status(500).send('Server Error');
//       } else {
//           res.render('filewatcher', { file_logs: data });
//       }
//   });
// });

router.get('/filewatcher', function(req, res) {
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
      var path = (watch_paths.length > 0) ? watch_paths[0].path : 'Default Path';
      // path değerini ve file_logs verisini ejs dosyasına gönder
      res.render('filewatcher', { path: path, file_logs: file_logs });
    });
  });
});

router.post('/your-path', function(req, res) {
  var filePath = req.body.filePath;
  // filePath ile istediğiniz işlemi yapabilirsiniz
  res.send('Dosya yolu alındı: ' + filePath);
});

// router.get('/filewatcher', function(req, res, next) {
//   res.render('filewatcher');
// });

// router.get('/news', function(req, res, next) {
//   res.render('news');
// });

// router.get('/network', function(req, res) {
//   res.render('network');
// });

// Router nesnesini dışa aktarın
module.exports = router;

