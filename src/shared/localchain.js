import elasticsearch from 'elasticsearch'
import _ from 'lodash'

const client = new elasticsearch.Client({ host: 'localhost:9200' })

global.client = client

const getGames = async () => {
    const gameIndex = await client.search({
        index: 'games',
        type: 'root'
    })
    return _.map(gameIndex.hits.hits, '_source')
}

const getGame = async (address) => {
    const gameIndex = await client.search({
        index: 'games',
        type: 'root',
        body: {
            query: {
                match: {
                    'receipt.contractAddress': address
                }
            }
        }
    })
    return gameIndex.hits.hits ? gameIndex.hits.hits[0]._source : {}
}

const getPublishers = async () => {
    const publisherIndex = await client.search({
        index: 'publishers',
        type: 'root'
    })
    return _.map(publisherIndex.hits.hits, '_source')
}

export {
    getGame,
    getGames,
    getPublishers,
}
