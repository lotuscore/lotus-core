import { Component } from 'react'
import PropTypes from 'prop-types'

import template from './template.rt'
import './styles.scss'


class PublisherDetails extends Component {
    constructor(props) {
        super(props)
        this.state = { publisher: this.props.address }
    }

    componentWillMount() {
        this.onChangeAccount()
    }

    onChangeAccount() {
        if (!this.props.local) return
        const updateAccount = async () => {
            const account = (await this.props.web3.eth.getAccounts())[0]
            this.setState({
                account,
                owner: account.toUpperCase() === this.state.publisher.toUpperCase()
            })
        }
        updateAccount()
    }

    render() {
        return template.call(this)
    }
}


PublisherDetails.contextTypes = {
    web3: PropTypes.object
}

export { PublisherDetails }
