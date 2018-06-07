import React, { Component } from 'react'
import Web3 from 'web3'

class Web3Provider extends Component {
    constructor(props, context) {
        super(props)
        this.state = {}
    }
    componentWillMount() {
        const request = new XMLHttpRequest()
        // curl --user bitcoinrpc:xxxxxxxxxxxxxxx --data-binary '{"jsonrpc":"1.0","id":"curltext","method":"getinfo","params":[]}' -H 'content-type:text/plain;' http://127.0.0.1:8332
        request.open('GET', "http://localhost:8545", true)
        request.onload = () =>  {
            this.setState({
                local: true,
                web3: new Web3(
                    new Web3.providers.HttpProvider("http://localhost:8545"))
            })
        }
        request.onerror = (e, q) => {
            const infuraToken = 'aWqldH9uqOpvc1tsATMl'
            this.setState({
                local: false,
                web3: new Web3(new Web3.providers.HttpProvider(
                               `https://mainnet.infura.io/${infuraToken}`))
            })
        };
        request.send()
    }
    render() {
        let app
        if (this.state.web3 === undefined) {
            app = <p>loading</p>
        } else {
            app = <this.props.component
                    web3={this.state.web3}
                    local={this.state.local}
                    address={this.props.match.params.address} />
        }
        return (<div>{ app }</div>)
    }
}

export default Web3Provider
