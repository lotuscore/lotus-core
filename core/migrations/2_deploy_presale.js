/* globals  artifacts */
const assert = require('assert')
const Cartridge = artifacts.require('./Cartridge.sol')
const Library = artifacts.require('./Library.sol')

module.exports = function(deployer) {
  const now = Math.round(new Date().getTime() / 1000)
  deployer.deploy(Cartridge)
  deployer.deploy(Library)
};
