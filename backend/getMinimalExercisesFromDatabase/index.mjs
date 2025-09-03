// LAMBDA IS NO LONGER NEEDED DUE TO MIGRATION OF DB TO SUPABASE
import pkg from 'pg';

const { Pool } = pkg;

// Create a single pool instance so it's reused across Lambda invocations
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  ssl: {
    rejectUnauthorized: false // Needed for RDS over SSL
  },
});

const query = `
  SELECT id, name, primary_muscle, beginner_friendly, equipment, rep_range
  FROM exercises
  WHERE NOT hidden
  ORDER BY name;
`;

export const handler = async (event) => {
  let client;
  try {
    // Borrow a client from the pool
    client = await pool.connect();

    const result = await client.query(query);

    return {
      statusCode: 200,
      headers: { 
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
      },
      body: JSON.stringify({ exercises: result.rows }),
    };
  } catch (error) {
    console.error("Error getting exercises:", error);
    return {
      statusCode: 500,
      headers: { 
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
      },
      body: JSON.stringify({ error: "Failed to fetch exercises" }),
    };
  } finally {
    // Release client back to the pool (important!)
    if (client) client.release();
  }
};