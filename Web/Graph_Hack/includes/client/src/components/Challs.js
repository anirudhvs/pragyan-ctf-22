import React, {Component, Fragment} from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/react-hooks';
import ChallItem from './ChallItem'


const CHALL_QUERY = gql`
    query ChallQuery {
        getAllChalls {
            id
            name
            domain
            key
        }
    }
`;

function Challs() {
    const {loading, error, data} = useQuery(CHALL_QUERY);
    if(loading) {
        return <h4>Loading...</h4>
    }
    if(error) {
        return <h4>Error!</h4>
    }
    return (
        data.getAllChalls.map(chall => (
            <ChallItem key={chall.id} chall={chall}/>
        ))
    )
}

export default Challs;
