// LAMBDA IS NO LONGER NEEDED DUE TO MIGRATION OF DB TO SUPABASE
import pkg from 'pg';
const { Pool } = pkg;

let pool;

export const handler = async (event) => {
  try {
    // Parse event body
    const body = event.body ? JSON.parse(event.body) : {};
    const exerciseId = body.exerciseId;

    if (!exerciseId) {
      return { 
        statusCode: 400, 
        headers: { 
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ error: "exerciseId is required" }) 
      };
    }

    // Create pool once
    if (!pool) {
      pool = new Pool({
        user: process.env.DB_USER,
        host: process.env.DB_HOST,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        ssl: { rejectUnauthorized: false },
      });
    }

    // Use pool.query() — returns a Promise
    const { rows } = await pool.query('SELECT * FROM exercises WHERE id = $1', [exerciseId]);
    const exercise = rows[0];

    if (!exercise) {
      return { 
        statusCode: 404, 
        headers: { 
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ error: "Exercise not found" }) 
      };
    }

    return { 
      statusCode: 200, 
      headers: { 
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(exercise) };

  } catch (error) {
    console.error("Error fetching exercise:", error);
    return { 
      statusCode: 500, 
      headers: { 
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
      },
      body: JSON.stringify({ error: "Internal server error" }) };
  }
};
