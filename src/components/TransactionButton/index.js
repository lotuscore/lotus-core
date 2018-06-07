import { Component } from 'react'
import PropTypes from 'prop-types'

import template from './template.rt'
import './styles.scss'


class TransactionButton extends Component {
    constructor(props) {
        super(props)
        this.sendTransaction = this.sendTransaction.bind(this)
    }

    componentWillMount() {
        this.onChangeAccount()
    }

    onChangeAccount() {
        if (!this.props.local) return
        const updateAccount = async () => {
            const account = (await this.props.web3.eth.getAccounts())[0]
            this.setState({ account })
        }
        updateAccount()
    }

    sendTransaction() {
        this.props.web3.eth.sendTransaction({
            from: this.state.account,
            to: this.props.address,
            value: this.props.amount
        })
        .then(function(receipt){
            console.log('receipt', receipt)
        })
    }

    render() {
        return template.call(this)
    }
}


TransactionButton.contextTypes = {
    web3: PropTypes.object
}

export { TransactionButton }
