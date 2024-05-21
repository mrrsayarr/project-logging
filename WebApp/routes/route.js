
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

router.get('/network', function(req, res) {
  db.readDataFromTable('IpLogs', function(err, data) {
      if (err) {
          console.error(err);
          res.status(500).send('Server Error');
      } else {
          res.render('network', { IpLogs: data }); // 'events' değişkeni burada tanımlanır
      }
  });
});

// router.get('/network', function(req, res) {
//   res.render('network');
// });

// Router nesnesini dışa aktarın
module.exports = router;

