const { gql } = require('apollo-server-express')

const typeDefs = gql`
enum Domain {
    WEB
    CRYPTOGRAPHY
    BINARY
    FORENSICS
    MISCELLANEOUS
}

type Chall {
    id: ID!
    name: String!
    domain: Domain!
    key: String!
}

input NewChallInput {
    name: String!
    domain: Domain!
    key: String!
}

type Query {
    superSecretQuery: String
    getAllChalls: [Chall]
    getChall(id: ID!): Chall
}

type Mutation {
    createChall(input: NewChallInput!): Chall
}
`

module.exports = typeDefs;