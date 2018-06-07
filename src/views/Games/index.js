import { Component } from 'react'
import template from './template.rt'
import './styles.scss'

import { getGames } from '../../shared/localchain'

class Games extends Component {
    constructor(props) {
        super(props)
        this.state = { games: [] }
    }
    componentWillMount() {
        (async () => {
            this.setState({ games: await getGames() })
        })()
    }
    render() {
        return template.call(this)
    }
}

export default Games
