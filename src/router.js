import React from 'react'
import { Route, Redirect } from 'react-router'

import Cartridge from './views/Cartridge'
import Game from './views/Game'
import Games from './views/Games'
import Publisher from './views/Publisher'
import Publishers from './views/Publishers'

import Web3Provider from './shared/components/Web3Provider'

export default (
  <div>
    <Route exact path="/" render={() => (
        <Redirect to="/games"/>
    )}/>
    <Route exact path="/publishers"
      render={(props) => <Web3Provider {...props} component={ Publishers } />} />
    <Route exact path="/publishers/:address"
      render={(props) => <Web3Provider {...props} component={ Publisher } />} />
    <Route exact path="/cartridges/:address"
      render={(props) => <Web3Provider {...props} component={ Cartridge } />} />
    <Route exact path="/games"
      render={(props) => <Web3Provider {...props} component={ Games } />} />
    <Route exact path="/games/:address"
      render={(props) => <Web3Provider {...props} component={ Game } />} />
  </div>
)
