const Chall = require('./models/Chall.model')
const resolvers = {
    Query: {
        superSecretQuery: () => {
            return 'pctf{gr4ph_ru1e5_th3_w0r1d}'
        },
        getAllChalls: async () => {
            return await Chall.find();
        },
        getChall: async (_parent, { id }, _context, _info) => {
            return await Chall.findById(id);
        }
    },
    Mutation: {
        createChall: async(parent, args, context, info) => {
            console.log(args);
            const {name, domain, key} = args.input;
            console.log(name, domain, key);
            const chall = new Chall({name, domain, key});
            await chall.save();
            return chall;
        }
    }
};

module.exports = resolvers;