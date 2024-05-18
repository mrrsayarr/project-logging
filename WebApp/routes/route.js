
var express = require('express');
var router = express.Router();

// Rotalarınızı burada tanımlayın
router.get('/', function(req, res) {
  res.render('index');
});

router.get('/eventlog', function(req, res) {
  res.render('eventlog');
});



// Router nesnesini dışa aktarın
module.exports = router;

