
var express = require('express');
var router = express.Router();
var db = require('../db'); // db.js dosyasını import
const axios = require('axios');
const { exec } = require('child_process');

// Middleware fonksiyonu ?
// function logRequest(req, res, next) {
//   console.log(`Received a request at ${new Date().toISOString()}`);
//   next();
// }
//router.use(logRequest);

// Rotaları burda yaz

router.get('/', function(req, res) {
  try {
    db.readDataFromTable('IpLogs', function(err, data) {
      if (err) {
        console.error(err);
        res.status(500).send('Server Error');
      } else {
        // 'events' veritabanından alınan veriyi temsil ediyorsa, bu veriyi almak için bir veritabanı sorgusu yapmanız gerekiyor
        db.readDataFromTable('Events', function(err, events) {
          if (err) {
            console.error(err);
            res.status(500).send('Server Error');
          } else {
            // 'index' görünümüne 'IpLogs', 'isGlobalIP' ve 'events' değişkenlerini gönder
            res.render('index', { IpLogs: data, isGlobalIP: isGlobalIP, events: events });
          }
        });
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

//----------------------------------------------

// Python Scripts Run

// const PythonShell = require('python-shell').PythonShell;

// let pythonShell;

// router.post('/run-python', (req, res) => {
//     let options = {
//         mode: 'text',
//         pythonPath: 'C:\\Users\\muham\\OneDrive\\Masaüstü\\proje\\securitydatasets\\2022.08.03\\master\\.venv\\Scripts\\python.exe',
//         pythonOptions: ['-u'],
//         scriptPath: 'C:\\Users\\muham\\OneDrive\\Masaüstü\\proje\\securitydatasets\\2022.08.03\\master\\',
//         args: []
//     };

//     pythonShell = PythonShell.run('LogCollector.py', options, function (err, results) {
//         if (err) {
//             console.error(`exec error: ${err}`);
//             return;
//         }
//         console.log('results: %j', results);
//     });

//     res.send('Python script is running');
// });

// router.post('/stop-python', (req, res) => {
//     if (pythonShell) {
//         pythonShell.end(function (err,code,signal) {
//             if (err) throw err;
//             console.log('The exit code was: ' + code);
//             console.log('The exit signal was: ' + signal);
//             console.log('finished');
//             console.log('finished');
//         });
//         res.send('Python script has been stopped');
//     } else {
//         res.send('No Python script is running');
//     }
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
        // console.log(data);
        res.render('eventlog', { events: data }); // 'events' değişkeni burada tanımlanır
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// isGlobalIP fonksiyonunu router.get('/network', ...) dışında tanımlayın
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

router.get('/network', function(req, res) {
  try {
    db.readDataFromTable('IpLogs', function(err, data) {
      if (err) {
        console.error(err);
        res.status(500).send('Server Error');
      } else {
        // 'events' veritabanından alınan veriyi temsil ediyorsa, bu veriyi almak için bir veritabanı sorgusu yapmanız gerekiyor
        db.readDataFromTable('Events', function(err, events) {
          if (err) {
            console.error(err);
            res.status(500).send('Server Error');
          } else {
            // 'index' görünümüne 'IpLogs', 'isGlobalIP' ve 'events' değişkenlerini gönder
            res.render('network', { IpLogs: data, isGlobalIP: isGlobalIP, events: events });
          }
        });
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
        res.redirect('/filewatcher');
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

// About 
router.get('/about', function(req, res) {
  try {
    res.render('about');
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

//----------------------------------------------

// Data Breach Page
router.get('/databreach', async (req, res) => {
  let data = null;
  let error = null;
  if (req.query.email) {
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

// Export the router 
module.exports = router;

