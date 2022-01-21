import React from 'react';
import gql from 'graphql-tag';
import { useMutation } from '@apollo/react-hooks'

const CHALL_MUTATION = gql`
    mutation createNewChall($input: NewChallInput!) {
            createChall(input: $input) {
                id
                name
                domain
                key
            }
    }
`;

const CreateChall = () => {
    let name, domain, key;
    const [createChall, { data, loading, error }] = useMutation(CHALL_MUTATION);
    return (
        <div>
            <form onSubmit={ e => {
                e.preventDefault();
                createChall({variables: {input: {name: name.value, domain: domain.value, key: key.value}}});
                window.location.reload();
            }}>
                <label> Name </label>
                <input ref={value => name = value} id="name"></input>
                <label> Domain </label>
                <input ref={value => domain = value} id="domain"></input>
                <label> Key </label>
                <input ref={value => key = value} id="key"></input>
                <button type="submit">Add Chall</button>
            </form>
        </div>
    )
}

export default CreateChall;