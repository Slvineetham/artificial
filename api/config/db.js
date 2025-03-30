const{ Pool } = require('pg');
require('dotenv').config();
const {
    DB_USER,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    JWT_SECRET_KEY,
    } = process.env

const pool = new Pool({
user:DB_USER,
host:DB_HOST,
database:DB_NAME,
password:DB_PASSWORD,
port:DB_PORT,
});
console.log("pool-",pool);
console.log("db");

// class Damage {

//     static async findDamage() {
      
//       const {rows} = await pool.query('SELECT * FROM public.damage_data');
//       console.log("rows",rows);
//         return rows;
//      }
//   }
  module.exports = pool;
  
  

// function(err) {
//   if (err) throw err;
//   console.log("Connected!");
  