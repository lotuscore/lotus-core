# Lotus Core #

### Getting Started

### Install OS requirements:

- **elasticsearch** [https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html]()
- **ganache-cli** [https://github.com/trufflesuite/ganache-cli]()
- **solc** [http://solidity.readthedocs.io/en/v0.4.24/installing-solidity.html]()
- **truffle** [http://truffleframework.com/docs/getting_started/installation]()
- **yarn** [https://yarnpkg.com/lang/en/]()

### Setup Project

```
> yarn install
> truffle compile
```

### Start Project

```
> ganache-cli
> yarn start
```

To start deploying a Game contract go to `/publishers/<given-ganache-public-address>` in the local server and start to test!

The explorer idea is to make queries over a local (and smaller) copy of the blockchain, this copy is over elasticsearch, and to synchronize it with the current blockchain state it is necessary to execute `yarn syncdb` each time.

### Run tests:

```
> truffle tests
```
