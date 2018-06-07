import { Component } from 'react'
import template from './template.rt'
import './styles.scss'

class Cartridge extends Component {
    render() {
        return template.call(this)
    }
}

export default Cartridge
