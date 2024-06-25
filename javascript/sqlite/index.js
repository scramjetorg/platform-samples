const http = require('http');
const qs = require('querystring');
const sqlite3 = require('sqlite3');
const path = require('path');

// Assuming the database structure is defined in prime.js
const dbPath = path.join(__dirname, 'products.db');; // Replace with the actual path to the database file
module.exports = async function (input) {
    const db = new sqlite3.Database(dbPath);

    // Function to query the database and extract the product list
    async function extractProductList(query) {
        return new Promise((res, rej) => {
            db.all(query, (err, rows) => {
                if (err) {
                    rej(err);
                } else {
                    res(rows);
                }
            });
        });
    }
    
    const server = http.createServer((req, res) => {
        res.setHeader('Content-Type', 'application/json');
        
        try {
            const { category } = qs.parse(req.url.split('?')[1]);
            
            let query;
            if (category) {
                query = `SELECT sku, msrp, name FROM products WHERE category = '${category}'`;
            } else {
                query = `SELECT sku, msrp, name FROM products`;
            }
            extractProductList(query)
                .then((rows) => {
                    res.statusCode = 200;
                    res.end(JSON.stringify(rows));
                })
                .catch((error) => {
                    res.statusCode = 500;
                    res.end(JSON.stringify({ error: 'Query Error', message: error.message }));
                });
            
        } catch (error) {
            res.statusCode = 500;
            res.end(JSON.stringify({ error: 'Internal Server Error', message: error.message }));
        }
    });

    server.listen(9080, () => {
        console.log('Server is listening on port 9080');
    });

    await new Promise((res, rej) => {
        server.on('close', res);
        server.on('error', rej);
    });
    
    db.close();
};
