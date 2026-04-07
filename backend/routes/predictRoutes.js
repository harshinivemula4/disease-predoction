const express = require("express");
const router = express.Router();
const axios = require("axios");

router.post("/predict", async (req, res) => {

  try {

    const symptoms = req.body.symptoms;

    const response = await axios.post("http://localhost:8000/predict", {
      symptoms: symptoms
    });

    res.json(response.data);

  } catch (error) {
    console.log(error);
    res.status(500).json({message:"Prediction error"});
  }

});

module.exports = router;