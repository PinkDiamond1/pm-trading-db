from gnosisdb.settings.local import *

GNOSISDB_CONTRACTS = {
    '254dffcd3277c0b1660f6d42efbb754edababc2b': {
        'name': 'Centralized Oracle Factory', # optional
        'factoryEventABI': '[{"inputs": [{"type": "bytes", "name": "ipfsHash"}], "constant": false, "name": "createCentralizedOracle", "payable": false, "outputs": [{"type": "address", "name": "centralizedOracle"}], "type": "function"}, {"inputs": [{"indexed": true, "type": "address", "name": "creator"}, {"indexed": false, "type": "address", "name": "centralizedOracle"}, {"indexed": false, "type": "bytes", "name": "ipfsHash"}], "type": "event", "name": "CentralizedOracleCreation", "anonymous": false}]',
        'instanceABI': '[{"inputs": [], "constant": true, "name": "outcome", "payable": false, "outputs": [{"type": "int256", "name": ""}], "type": "function"}, {"inputs": [{"type": "int256", "name": "_outcome"}], "constant": false, "name": "setOutcome", "payable": false, "outputs": [], "type": "function"}, {"inputs": [], "constant": true, "name": "getOutcome", "payable": false, "outputs": [{"type": "int256", "name": ""}], "type": "function"}, {"inputs": [], "constant": true, "name": "owner", "payable": false, "outputs": [{"type": "address", "name": ""}], "type": "function"}, {"inputs": [{"type": "address", "name": "newOwner"}], "constant": false, "name": "replaceOwner", "payable": false, "outputs": [], "type": "function"}, {"inputs": [], "constant": true, "name": "ipfsHash", "payable": false, "outputs": [{"type": "bytes", "name": ""}], "type": "function"}, {"inputs": [], "constant": true, "name": "isSet", "payable": false, "outputs": [{"type": "bool", "name": ""}], "type": "function"}, {"inputs": [], "constant": true, "name": "isOutcomeSet", "payable": false, "outputs": [{"type": "bool", "name": ""}], "type": "function"}, {"inputs": [{"type": "address", "name": "_owner"}, {"type": "bytes", "name": "_ipfsHash"}], "type": "constructor", "payable": false}, {"inputs": [{"indexed": true, "type": "address", "name": "newOwner"}], "type": "event", "name": "OwnerReplacement", "anonymous": false}, {"inputs": [{"indexed": false, "type": "int256", "name": "outcome"}], "type": "event", "name": "OutcomeAssignment", "anonymous": false}]',
        'factoryEventSerializer': 'relationaldb.serializers.CentralizedOracleSerializer', # new CentralizedOracleCreation
        'instanceAddressesGetter': None, # todo discuss: better than accessing this, get factory by searching Contract.get(address=)
        'instanceEventSerializer': None # todo implement instance serializers and models
    }
}

ETHEREUM_NODE_HOST='localhost'
ETHEREUM_NODE_PORT = 8545
ETHEREUM_NODE_SSL = 0

# IPFS
IPFS_HOST = '192.168.1.165'
IPFS_PORT = 5001