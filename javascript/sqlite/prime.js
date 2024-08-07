#!/usr/bin/env node

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Create a new database connection
const dbPath = path.join(__dirname, 'products.db');
const db = new sqlite3.Database(dbPath);

// Create the "products" table
db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sku TEXT,
            category TEXT,
            wholesale_price REAL,
            cost_of_sale REAL,
            msrp REAL
        )
    `);
});
// Generate 15 products for a petrol station
const products = [
    { name: 'Coca-Cola', sku: 'COKE001', wholesale_price: 0.50, cost_of_sale: 0.30, msrp: 1.00, category: 'Beverage' },
    { name: 'Pepsi', sku: 'PEPSI001', wholesale_price: 0.50, cost_of_sale: 0.30, msrp: 1.20, category: 'Beverage' },
    { name: 'Verva Energy', sku: 'VERVA001', wholesale_price: 0.50, cost_of_sale: 0.30, msrp: 1.10, category: 'Beverage' },
    { name: 'Fanta', sku: 'FANTA001', wholesale_price: 0.50, cost_of_sale: 0.30, msrp: 1.30, category: 'Beverage' },
    { name: 'KitKat', sku: 'KITKAT001', wholesale_price: 0.30, cost_of_sale: 0.20, msrp: 0.80, category: 'Snack' },
    { name: 'Snickers', sku: 'SNICKERS001', wholesale_price: 0.30, cost_of_sale: 0.20, msrp: 0.90, category: 'Snack' },
    { name: 'Mars', sku: 'MARS001', wholesale_price: 0.30, cost_of_sale: 0.20, msrp: 0.85, category: 'Snack' },
    { name: 'Twix', sku: 'TWIX001', wholesale_price: 0.30, cost_of_sale: 0.20, msrp: 0.95, category: 'Snack' },
    { name: 'Yoplait', sku: 'YOPLAIT001', wholesale_price: 0.80, cost_of_sale: 0.50, msrp: 1.70, category: 'Dairy' },
    { name: 'Danone', sku: 'DANONE001', wholesale_price: 0.80, cost_of_sale: 0.50, msrp: 1.60, category: 'Dairy' },
    { name: 'Activia', sku: 'ACTIVIA001', wholesale_price: 0.80, cost_of_sale: 0.50, msrp: 1.80, category: 'Dairy' },
    { name: 'Castrol', sku: 'CASTROL001', wholesale_price: 5.00, cost_of_sale: 3.50, msrp: 12.00, category: 'Automotive' },
    { name: 'Mobil 1', sku: 'MOBIL001', wholesale_price: 5.00, cost_of_sale: 3.50, msrp: 11.00, category: 'Automotive' },
    { name: 'Shell Helix', sku: 'SHELL001', wholesale_price: 5.00, cost_of_sale: 3.50, msrp: 13.00, category: 'Automotive' },
    { name: 'Valvoline', sku: 'VALVOLINE001', wholesale_price: 5.00, cost_of_sale: 3.50, msrp: 10.50, category: 'Automotive' }
];

// Insert the products into the "products" table
db.serialize(() => {
    const stmt = db.prepare(`
        INSERT INTO products (name, sku, wholesale_price, cost_of_sale, category, msrp)
        VALUES (?, ?, ?, ?, ?, ?)
    `);
    products.forEach(product => {
        stmt.run(product.name, product.sku, product.wholesale_price, product.cost_of_sale, product.category, product.msrp);
    });
    stmt.finalize();
});

// Close the database connection
db.close();
