
var express = require('express');
var router = express.Router();
var db = require('../db'); // db.js dosyasını import
const axios = require('axios');

// Middleware fonksiyonu ?
// function logRequest(req, res, next) {
//   console.log(`Received a request at ${new Date().toISOString()}`);
//   next();
// }
//router.use(logRequest);

// Rotaları burda yaz

router.get('/', function(req, res, next) {
  db.getLastTenEvents(function(events) { // db.getLastTenEvents fonksiyonunu kullanın
    res.render('index', { events: events });
  });
});

//----------------------------------------------

// Data Breach Page
router.get('/databreach', async (req, res) => {
  let data = null;
  let error = null;
  console.log('ROUTER');
  if (req.query.email) {
    console.log('IF');
    try {
      const response = await axios.get(`https://haveibeenpwned.com/api/v3/breachedaccount/${req.query.email}`, {
        headers: {
          'hibp-api-key': 'YOUR_HIBP_API_KEY' // Buraya Have I Been Pwned'den aldığınız API anahtarınızı girin
        }
      });
      data = response.data;
    } catch (err) {
      console.error(err);
      error = 'An error occurred while checking for breaches.';
    }
  }

  res.render('databreach', { data, error });
});

//----------------------------------------------

// // Python Scripts Run
// let intervalId;

// // Python scriptini her 30 saniyede bir çalıştıran işlem
// intervalId = setInterval(function() {
//   const { spawn } = require('child_process');
//   // const python = spawn('python', ['../../master/FileWatchdog.py']);
//   const python = spawn('python', ["C:\\Users\\muham\\OneDrive\\Masaüstü\\proje\\securitydatasets\\2022.08.03\\master\\FileWatchdog.py"]);
  
//   python.stdout.on('data', (data) => {
//     console.log(`stdout: ${data}`);
//   });

//   python.stderr.on('data', (data) => {
//     console.error(`stderr: ${data}`);
//   });

//   python.on('close', (code) => {
//     console.log(`child process exited with code ${code}`);
//   });
// }, 30000);  // 30000 milisaniye = 30 saniye

// // Butonla tetiklenecek route
// router.get('/run-python', function(req, res) {
//   const { spawn } = require('child_process');
//   // const python = spawn('python', ['../../master/FileWatchdog.py']);
//   const python = spawn('python', ["C:\\Users\\muham\\OneDrive\\Masaüstü\\proje\\securitydatasets\\2022.08.03\\master\\FileWatchdog.py"]);

//   python.stdout.on('data', (data) => {
//     console.log(`stdout: ${data}`);
//   });

//   python.stderr.on('data', (data) => {
//     console.error(`stderr: ${data}`);
//   });

//   python.on('close', (code) => {
//     console.log(`child process exited with code ${code}`);
//     res.send(`Python script exited with code ${code}`);
//   });
// });

// // Python scriptini durdurma route'u
// router.get('/stop-python', function(req, res) {
//   clearInterval(intervalId);
//   res.send('Python script stopped');
// });

//----------------------------------------------

// Event log Collector and Analyzer
router.get('/eventlog', function(req, res) {
  try {
    db.readDataFromTable('events', function(err, data) {
      if (err) {
        console.error(err);
        res.status(500).send('Server Error');
      } else {
        res.render('eventlog', { events: data }); // 'events' değişkeni burada tanımlanır
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// IpLogs 
router.get('/network', function(req, res) {
  function isGlobalIP(ip) {
    const parts = ip.split('.');
    if (parts.length !== 4) {
      // Not a valid IP address
      return false;
    }

    if (parts[0] === '10') {
      return false;
    }

    if (parts[0] === '172' && parts[1] >= 16 && parts[1] <= 31) {
      return false;
    }

    if (parts[0] === '192' && parts[1] === '168') {
      return false;
    }

    if (parts[0] === '127' && parts[1] === '0' && parts[2] === '0' && parts[3] === '1') {
      // Localhost IP address
      return false;
    }

    // Assume any other IP is a global IP
    return true;
  }

  try {
    db.readDataFromTable('IpLogs', function(err, data) {
      if (err) {
        console.error(err);
        res.status(500).send('Server Error');
      } else {
        res.render('network', { IpLogs: data, isGlobalIP: isGlobalIP }); // 'IpLogs' ve 'isGlobalIP' değişkenleri burada tanımlanır
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// Cyber Security News
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

// File Watchdog - File Logs
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


// File Logs - File Watchdog
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

      var path = watch_paths[0].path;
      res.render('filewatcher', { path: path, file_logs: file_logs });
    });
  });
});

// File Watcher Path Changer
router.post('/update-path', function(req, res) {
  try {
    var newPath = req.body.newPathInput;

    var tableName = 'watch_paths';
    var updates = { path: newPath };
    var condition = 'id = 1';

    db.updateDataInTable(tableName, updates, condition, function(err) {
      if (err) {
        console.error(err);
        res.status(500).send('Server Error');
        console.log('error: ' + err.message);
      } else {
        console.log('Row(s) updated: 1');
        res.redirect('/');
        console.log('Succesfully updated path!');
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// Virustotal 
router.get('/virustotal', function(req, res) {
  try {
    res.render('virustotal');
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});


// Export the router 
module.exports = router;

