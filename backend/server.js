const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const predictRoutes = require("./routes/predictRoutes");
const authRoutes = require("./routes/authRoutes");

const app = express();

app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://localhost:27017/diseaseDB")
.then(() => console.log("MongoDB Connected"))
.catch(err => console.log(err));

app.use("/api", authRoutes);

// root test route
app.get("/", (req, res) => {
  res.send("Disease Prediction Backend Running");
});
app.use("/api", predictRoutes);

app.listen(5000, () => {
  console.log("Server running on port 5000");
});