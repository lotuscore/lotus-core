const contract = require('truffle-contract')
const elasticsearch = require('elasticsearch')
const Web3 = require('web3')
const _ = require('lodash')

const GameContract = require('../build/contracts/Game.json')

const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
const Game = contract(GameContract)

const bin = '0x606060405234156200001057600080fd5b604051620026ec380380620026ec833981016040528080518201919060200180'

const isAGameContact = (input) => {
    return input.substring(0, 100) === bin
}

// setup blockchain
Game.setProvider(web3.currentProvider)
fixTruffleContractCompatibilityIssue(Game)

// setup elasticsearch
const client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
})

const type = 'root'

const setup = async () => {
    const configExist = await client.exists({
        index: 'config',
        id: '1',
        type
    })
    if (!configExist) {
        await client.create({
            index: 'config',
            id: '1',
            type,
            body: {'last_block': 0}
        })
    }
}

const retrieveTransactions = async () => {
    const startBlockNumber = (await client.get({
        index: 'config',
        id: '1', type,
    }))._source.last_block
    const endBlockNumber = (await web3.eth.getBlockNumber()) + 1

    for (let i = startBlockNumber; i < endBlockNumber; i++) {
        const block = await web3.eth.getBlock(i, true);

        if (block != null && block.transactions != null) {
            block.transactions.forEach(async (e) => {
                if (isAGameContact(e.input)) {
                    const receipt = await web3.eth.getTransactionReceipt(e.hash)
                    const game = Game.at(receipt.contractAddress)
                    const gameInstance = {
                        title: await game.title(),
                        projectUrl: await game.projectUrl(),
                        classification: await game.classification(),
                        status: await game.status(),
                        price: await game.price(),
                        genre: await game.genre(),
                        rating: await game.rating(),
                        platforms: await game.platforms(),
                        data: await game.data(),
                        signGuard: await game.signGuard(),
                        publisher: await game.publisher(),
                        token: await game.token()
                    }

                    client.index({
                        index: 'games',
                        id: e.hash,
                        type,
                        body: {
                            transaction: e,
                            receipt: receipt,
                            instance: gameInstance
                        }
                    })

                    client.create({
                        index: 'publishers',
                        id: gameInstance.publisher,
                        type,
                        body: {
                            address: gameInstance.publisher
                        }
                    })
                }
            })
        }
    }
    if (startBlockNumber !== endBlockNumber) {
        await client.index({
            index: 'config',
            id: '1',
            type,
            body: { last_block: endBlockNumber }
        })
    }
}

setup().then(retrieveTransactions)

function fixTruffleContractCompatibilityIssue(contract) {
    if (typeof contract.currentProvider.sendAsync !== "function") {
        contract.currentProvider.sendAsync = function() {
            return contract.currentProvider.send.apply(
                contract.currentProvider, arguments
            )
        }
    }
    return contract;
}
