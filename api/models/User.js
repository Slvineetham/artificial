const pool = require('../config/db');
const bcrypt = require('bcrypt');

class User {
  static async create(username, email, password) {
    const hashedPassword = await bcrypt.hash(password, 10);
    const { rows } = await pool.query(
      'INSERT INTO users (username, email, password) VALUES ($1, $2, $3) RETURNING *',
      [username, email, hashedPassword]
    );
    return rows[0];
  }

  static async findByEmail(email) {
    const { rows } = await pool.query('SELECT * FROM public.users WHERE email = $1', [email]);
    return rows[0];
  }

  // Add more methods (update, delete, etc.)
}
module.exports = User;
