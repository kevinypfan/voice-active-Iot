const mqtt = require('mqtt')
const mongoose = require('mongoose')
const express = require('express')
const cors = require('cors')
const path = require('path')
const Temp = require('./models/temp')
const app = express()
var client = mqtt.connect('mqtt broker')

mongoose.connect('mongodb://localhost/temp_hum', { useNewUrlParser: true }).then(() => {
    console.log("Connected to Database!")
}).catch((err) => {
    console.log("Not Connected to Database ERROR! ", err);
});
mongoose.set('useCreateIndex', true);

app.use(cors())
app.use('/', express.static('dist'));
app.get('/sensor/temp/:limit', (req, res) => {
    const limit = req.params.limit
    Temp.find().sort({ _id: -1 }).limit(parseInt(limit)).then(temp => {
        res.send(temp)
    })
})

app.get('/sensor/now/temp', (req, res) => {
    Temp.findOne().sort({ _id: -1 }).then(temp => {
        res.send(temp.ds18b20.temperature)
    });
})

app.get('/sensor/now/hum', (req, res) => {
    Temp.findOne().sort({ _id: -1 }).then(temp => {
        res.send(temp.dht11.humidity)
    });
})

app.get('*', (req, res) => {
    res.sendfile(path.resolve(__dirname, 'dist', 'index.html'))
})

app.listen(3000, () => {
    console.log(`🚀 Server ready at localhost:3000`);
})

client.on('connect', function () {
    client.subscribe('KevinFan/lab305/temp_hum')
})


client.on('message', function (topic, message) {
    // message is Buffer
    const topicAry = topic.split('/')
    switch (topicAry[2]) {
        case 'temp_hum':
            const data = JSON.parse(message.toString())
            data.timestamp = Date.now()
            const temp = new Temp(data)
            temp.save().then(result => {
                client.publish('KevinFan/lab305/update', JSON.stringify(result))
                console.log(result)
            })
            break;
    }
    console.log(JSON.parse(message.toString()))
})