const mongoose = require('mongoose');

const ChallSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    domain: {
        type: String,
        required: true,
    },
    key: {
        type: String,
        required: true,
    }
});

const Chall = mongoose.model('chall', ChallSchema);
module.exports = Chall;