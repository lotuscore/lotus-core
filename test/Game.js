/* globals web3, require, artifacts, contract, it, beforeEach, before */
import EVMRevert from 'zeppelin-solidity/test/helpers/EVMRevert';

const BigNumber = web3.BigNumber;
require('chai')
  .use(require('chai-as-promised'))
  .use(require('chai-bignumber')(BigNumber))
  .should();

const Game = artifacts.require('./Game.sol');
const StandardTokenMock = artifacts.require('./helpers/StandardTokenMock.sol');

const gamePrice = new BigNumber(100);
const genericGame = [
  'title',
  'https://projectUrl.com',
  0, // game
  1, // in development
  gamePrice,
  1, // action
  ['tag'],
  16, // allages
  7, // win, linux, mac
  'lfs://1234567890',
  false,
];
const useETH = 0;

contract('Game', (accounts) => {
  beforeEach(async function () {
    this.publisher = accounts[0];
    this.player = accounts[1];
    this.token = await StandardTokenMock.new(this.player, gamePrice);
  });
  describe('Sold in ethers', () => {
    beforeEach(async function () {
      this.game = await Game.new(
        ...genericGame,
        this.publisher,
        useETH
      ).should.be.fulfilled;
    });
    it('Should be able to buy using ethers', async function () {
      const value = await this.game.price.call();
      await this.game.buyGame({ from: this.player, value}
      ).should.be.fulfilled;
    });
    it('Should be able to buy using more ethers than required', async function () {
      const value = (await this.game.price.call()).mul(2);
      await this.game.buyGame({ from: this.player, value}
      ).should.be.fulfilled;
    });
    it('Should fails by not sending ethers', async function () {
      const value = 0;
      await this.game.buyGame({ from: this.player, value }
      ).should.be.rejectedWith(EVMRevert);
    });
    it('Should fails by sending less ethers than price', async function () {
      const value = (await this.game.price.call()).div(2);
      await this.game.buyGame({ from: this.player, value }
      ).should.be.rejectedWith(EVMRevert);
    });
    it('Should fails by sending tokens instead ethers', async function () {
      await this.game.buyGame({ from: this.player }
      ).should.be.rejectedWith(EVMRevert);
    });
  });
  describe('Sold in tokens', () => {
    beforeEach(async function () {
      this.game = await Game.new(
        ...genericGame,
        this.publisher,
        this.token.address
      ).should.be.fulfilled;
    });
    it('Should by able to buy using tokens', async function () {
      const allowance = await this.game.price.call();
      await this.token.approve(this.game.address, allowance, {
        from: this.player
      });
      await this.game.buyGame({
        from: this.player
      }).should.be.fulfilled;
    });
    it('Should fails approving less tokens than price', async function () {
      const allowance = (await this.game.price.call()).div(2);
      await this.token.approve(this.game.address, allowance, {
        from: this.player
      });
      await this.game.buyGame({ from: this.player }
      ).should.be.rejectedWith(EVMRevert);
    });
    it('Should fails paying using ethers', async function () {
      const value = await this.game.price.call();
      await this.game.buyGame({ from: this.player, value }
      ).should.be.rejectedWith(EVMRevert);
    });
  });
  describe('After purchase', () => {
    beforeEach(async function () {
      this.game = await Game.new(
        ...genericGame,
        this.publisher,
        useETH
      ).should.be.fulfilled;
      await this.game.buyGame(
        { from: this.player, value: gamePrice}
      ).should.be.fulfilled;
    });
    it('Should create a new Cartridge', async function () {
    });
  });
});
