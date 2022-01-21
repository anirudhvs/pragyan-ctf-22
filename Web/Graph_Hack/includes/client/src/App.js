import React from 'react';
import { InMemoryCache, ApolloClient} from '@apollo/client';
import { ApolloProvider } from '@apollo/react-hooks';
import Challs from './components/Challs';
import CreateChall from './components/CreateChall';
import './App.css';

const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql',
  cache: new InMemoryCache(),
});

function App() {
  return (
    <ApolloProvider client={client}>
        <div className="App">
          <Challs></Challs>
          <CreateChall></CreateChall>
        </div> 
    </ApolloProvider> 
    
  );
}

export default App;
