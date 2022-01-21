require("dotenv").config();

module.export = {
    env: {
        MONGO_URL=process.env.MONGO_URL,
        GRAPH_API_URL=process.env.GRAPH_API_URL,
    }
}