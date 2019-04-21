const express = require('express')
const app = express()
const path = require('path')

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '/results.html'))
})

app.listen(8080)