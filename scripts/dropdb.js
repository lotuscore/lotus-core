const elasticsearch = require('elasticsearch')

const client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
})

client.indices.delete({index: 'games'})
client.indices.delete({index: 'config'})
client.indices.delete({index: 'publishers'})
