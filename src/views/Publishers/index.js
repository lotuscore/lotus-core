import { Component } from 'react'
import template from './template.rt'
import './styles.scss'

import { getPublishers } from '../../shared/localchain'

class Publishers extends Component {
    constructor(props) {
        super(props)
        this.state = { publishers: [] }
    }
    componentWillMount() {
        (async () => {
            this.setState({ publishers: await getPublishers() })
        })()
    }
    render() {
        return template.call(this)
    }
}

export default Publishers
