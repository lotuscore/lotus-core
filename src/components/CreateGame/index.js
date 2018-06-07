import { Component } from 'react'
import PropTypes from 'prop-types'

import fixTruffleContractCompatibilityIssue from '../../shared/utils'
import GameContract from '../../../build/contracts/Game.json'
import template from './template.rt'
import './styles.scss'

import BigNumber from 'bignumber.js'

const contract = require('truffle-contract')
const Game = contract(GameContract)

class CreateGame extends Component {
  constructor(props) {
    super(props)

    Game.setProvider(props.web3.currentProvider)
    fixTruffleContractCompatibilityIssue(Game)

    this.state = {
      title: 'Test Game',
      projectUrl: 'http://projecturl.com',
      tagline: 'short description',
      description: 'long description',
      icon: 'base64icon===',
      classification: 0, // game
      status: 0, // released
      price: 100,
      genre: 1, // action
      tags: ['tag'],
      rating: 16,
      platforms: 1,
      data: 'magner://1234560',
      publisher: this.props.address,
      token: 0, // no token


      account: this.props.address,
      signGuard: false
    }

    this.set = this.set.bind(this)
    this.createGame = this.createGame.bind(this)
  }

  componentWillMount() {
    this.onChangeAccount()
  }

  onChangeAccount() {
    if (!this.props.local) return
    /*
    const account = global.web3.eth.accounts[0]
    const updateAccount = async () => {
      this.tokenInstance = await Game.deployed()

      const balance = await this.tokenInstance.balanceOf(account)
      const vaults = []

      this.setState({ account, balance, vaults })
    }
    updateAccount()
    */
  }

  set(key) {
    return (e) => {
      if (e.target.type === 'checkbox') {
        return this.setState({ [key]: e.target.checked })
      }
      this.setState({ [key]: e.target.value })
    }
  }

  createGame() {
      const genericGame = [
        'title',
        'https://projectUrl.com',
        0, // game
        1, // in development
        new BigNumber(100),
        1, // action
        [],
        16, // allages
        7, // win, linux, mac
        'magnet://1234567890',
        false
      ];


      const create = async () => {
        // console.log('create', Game)
        const gameInstance = await Game.new(
          ...genericGame,
          this.state.publisher,
          0, {
            from: this.state.account,
            gas: 4000000
          })
        console.log('gameInstance', gameInstance)
      }
      create()
  }

  render() {
    return template.call(this)
  }
}


CreateGame.contextTypes = {
  web3: PropTypes.object
}

export { CreateGame }
