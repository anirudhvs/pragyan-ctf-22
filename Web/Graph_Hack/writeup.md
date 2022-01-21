# Pragyan CTF 2022: GraphHack
## WriteUp
When exploring the website, the homepage displays the name, domain and keys of challenges. Form for adding new challenges is given.
![alt text](./assets/image2.png)

- On Intercepting the requests made by the site using tools like BurpSuite, it leads us to a graphql endpoint running on port 4000.
![alt text](./assets/image1.png)

- Making Queries to the same endpoint, gives us the similar response as the frontend.
![alt text](./assets/image3.png)

- Perform a GraphQL Introspection by sending a full request on the target, which will return the full schema of the server, including queries, mutations, objects, etc.
A Sample query is given below.
```
query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        args {
          ...InputValue
        }
        locations
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    } 
  }   
      
  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }     
        
  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
        }
      }
    } 
  }     
```
![alt text](./assets/image6.png)
![alt text](./assets/image7.png)
- Searching through the response for suspicious phrases, we get the following clue.
![alt text](./assets/image9.png)
Making the following query gives the flag for the challenge.
![alt text](./assets/image4.png)

Flag for the above challenge: 
```
pctf{gr4ph_ru1e5_th3_w0r1d}
```