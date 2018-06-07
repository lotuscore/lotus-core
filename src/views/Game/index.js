import { Component } from 'react'
import template from './template.rt'
import './styles.scss'

import { getGame } from '../../shared/localchain'

class Game extends Component {
    constructor(props) {
        super(props)
        this.state = { games: {} }
    }
    componentWillMount() {
        (async () => {
            this.setState({ game: await getGame(this.props.address) })
        })()
    }
    render() {
        return template.call(this)
    }
}

export default Game
