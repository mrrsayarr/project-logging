
// Veritabanına bağlantı işlemleri

const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('../master/Database.db', (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Veritabanına bağlandı');
});

function checkDbConnection() {
    db.get("SELECT 1", (err, row) => {
        if (err) {
            console.error('Veritabanına bağlantı başarısız:', err.message);
        } else {
            console.log('Veritabanına başarıyla bağlandı');
        }
    });
}

// Son 10 veriyi getir
function getLastTenEvents(callback) {
    let sql = `SELECT events.*, eventdescription.Description 
               FROM events 
               JOIN eventdescription ON events.EventID = eventdescription.EventID 
               ORDER BY events.EventID DESC 
               LIMIT 10`;
    db.all(sql, [], (err, rows) => {
      if (err) {
        throw err;
      }
      callback(rows);
    });
}

// Sadece belirli bir tablodaki verileri çekmek için fonksiyon (Mevcut: events)
// function readData() {
//     db.all("SELECT * FROM events", [], (err, rows) => {
//         if (err) {
//             throw err;
//         }
//         rows.forEach((row) => {
//             console.log(row);
//         });
//     });
// }

// const query = `SELECT * FROM ${tableName} ORDER BY EventID ASC`; // VERİLERİ SIRALAMAK İÇİN
const readDataFromTable = function(tableName, callback) {
    if (typeof callback !== 'function') {
        throw new Error('callback must be a function');
    }

    let query;
    if (tableName === 'events') {
    // 'events' tablosu için LEFT JOIN işlemi uygulanır
    query = `SELECT ${tableName}.*, eventdescription.Description 
        FROM ${tableName} 
        LEFT JOIN eventdescription ON ${tableName}.EventID = eventdescription.EventID 
        ORDER BY ${tableName}.PredictedValue DESC`;
    } else {
        // Diğer tablolar için basit bir SELECT sorgusu kullanılır
        query = `SELECT * FROM ${tableName}`;
    }

    db.all(query, function(error, results) {
        if (error) {
            console.error('Database error:', error);
            callback(error, null);
        } else {
            callback(null, results);
        }
    });
};


// IPLOGS VE DİĞER TABLOLAR İÇİN
function readDataFromAnotherTable(tableName) {
    db.all(`SELECT * FROM ${tableName}`, [], (err, rows) => {
        if (err) {
            throw err;
        }
        rows.forEach((row) => {
            console.log(row);
        });
    });
}


// Veri Ekleme
function insertDataIntoTable(tableName, data) {
    const keys = Object.keys(data).join(',');
    const values = Object.values(data).map(value => `'${value}'`).join(',');

    db.run(`INSERT INTO ${tableName} (${keys}) VALUES (${values})`, function(err) {
        if (err) {
            return console.error(err.message);
        }
        console.log(`A row has been inserted with rowid ${this.lastID}`);
    });
}

// Veri Silme
function deleteDataFromTable(tableName, condition) {
    db.run(`DELETE FROM ${tableName} WHERE ${condition}`, function(err) {
        if (err) {
            return console.error(err.message);
        }
        console.log(`Row(s) deleted ${this.changes}`);
    });
}

// Veri Güncelleme
function updateDataInTable(tableName, updates, condition) {
    const updateSet = Object.keys(updates).map(key => `${key}='${updates[key]}'`).join(',');

    db.run(`UPDATE ${tableName} SET ${updateSet} WHERE ${condition}`, function(err) {
        if (err) {
            return console.error(err.message);
        }
        console.log(`Row(s) updated: ${this.changes}`);
    });
}

// console.log(readData()); // Konsoldaki çıktıyı görmek için

// console.log(readDataFromAnotherTable('IpLogs'));

module.exports = {
    db,
    checkDbConnection,
    readDataFromTable,
    insertDataIntoTable,
    deleteDataFromTable,
    updateDataInTable,
    readDataFromAnotherTable,
    getLastTenEvents
};

