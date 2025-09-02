const { Client } = require('pg');

const client = new Client({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PWD,
  ssl: {
    rejectUnauthorized: false // For RDS, this is typically needed
  }
});

// serial means that primary key gets auto-incremented on record insertion unless
// exercise_id is specified
const createTableQuery = `
    CREATE TABLE IF NOT EXISTS exercises (
      exercise_id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      rep_range VARCHAR(50),
      sets INTEGER
    );
`;

exports.handler = async (event) => {
  try {
    await client.connect(); // establishes connection from Lambda function to the database
    await client.query(createTableQuery); // sends query to database
    await client.end(); // closes database connection once query complete

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Table created successfully." }),
    };
  } catch (error) {
    console.error("Error creating table:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Failed to create table." }),
    };
  }
};