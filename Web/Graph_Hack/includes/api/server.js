require('dotenv').config({path:__dirname+'/./../.env'})
const express = require('express')
const { ApolloServer } = require('apollo-server-express')
const {
    ApolloServerPluginLandingPageDisabled
  } = require("apollo-server-core");
const typeDefs = require('./schema')
const resolvers = require('./resolvers')
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

app.use(cors());

async function startServer() {
    const app = express();
    const server = new ApolloServer({
        typeDefs,
        resolvers,
        plugins: [
            ApolloServerPluginLandingPageDisabled(),
        ],
    });
    await server.start();
    server.applyMiddleware({app: app});
    app.use((req, res) => {
        res.send("Hello, Peter!");
    });
    await mongoose.connect(process.env.DB_URL, {
        useUnifiedTopology: true,
        useNewUrlParser: true,
    });
    console.log('Mongoose connected...');
    app.listen(4000, () => console.log('Server running on port 4000'));
}
startServer();