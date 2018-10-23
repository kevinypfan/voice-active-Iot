const mongoose = require('mongoose');


const schema = new mongoose.Schema({
    ds18b20: {
        temperature: {
            type: String
        }
    },
    timestamp: {
        type: Date
    },
    dht11: {
        temperature: {
            type: String
        },
        humidity: {
            type: String
        }
    }
})

module.exports = mongoose.model('Iot', schema);