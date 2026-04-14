const { Pool } = require('pg');
const fs = require('fs');
require('dotenv').config();

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function seed() {
    const data = JSON.parse(fs.readFileSync('./mock_data.json', 'utf8'));
    
    console.log('Seeding database...');
    
    // 1. Categories
    const categories = [...new Set(data.products.map(p => p.category))];
    const catMap = {};
    for (const cat of categories) {
        const res = await pool.query('INSERT INTO categories (name) VALUES ($1) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id', [cat]);
        catMap[cat] = res.rows[0].id;
    }

    // 2. Products
    for (const p of data.products) {
        await pool.query('INSERT INTO products (id, name, category_id, price, stock) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO NOTHING', 
            [p.id, p.name, catMap[p.category], p.price, p.stock]);
    }

    // 3. Customers
    for (const c of data.customers) {
        await pool.query('INSERT INTO customers (id, name, email, is_loyalty_member, created_at) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO NOTHING', 
            [c.id, c.name, c.email, c.is_loyalty_member, c.created_at]);
    }

    // 4. Orders
    for (const o of data.orders) {
        await pool.query('INSERT INTO orders (id, customer_id, total_amount, order_date) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING', 
            [o.id, o.customer_id, o.total_amount, o.order_date]);
    }

    // 5. Order Items
    for (const item of data.order_items) {
        await pool.query('INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES ($1, $2, $3, $4)', 
            [item.order_id, item.product_id, item.quantity, item.price_at_purchase]);
    }

    console.log('Seed complete.');
    await pool.end();
}

seed().catch(err => console.error(err));
