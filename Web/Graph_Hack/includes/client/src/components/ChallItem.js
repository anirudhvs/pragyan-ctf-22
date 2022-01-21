import React from 'react'

export default function ChallItem({chall: {id, name, domain, key}}) {
    return (
        <div>
            <h3>Name: {name}</h3>
            <h4>Domain: {domain}</h4>
            <h4>Key: {key}</h4>
            <hr></hr>
        </div>
    )
}