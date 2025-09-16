const express = require("express");
const { Client } = require("pg");

const app = express();

app.get("/", async (req, res) => {
  try {
    const client = new Client({
      host: "db",
      user: process.env.POSTGRES_USER || "user",
      password: process.env.POSTGRES_PASSWORD || "pass",
      database: process.env.POSTGRES_DB || "testdb"
    });
    await client.connect();
    const result = await client.query("SELECT NOW()");
    await client.end();
    res.send("📦 Hola desde Express! Hora en DB: " + result.rows[0].now);
  } catch (err) {
    res.send("Error conectando a DB: " + err);
  }
});

app.listen(process.env.PORT || "8080", () => console.log("Servidor en puerto " + process.env.PORT || "8080"));