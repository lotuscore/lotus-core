const fixTruffleContractCompatibilityIssue = (contract) => {
    if (typeof contract.currentProvider.sendAsync !== "function") {
        contract.currentProvider.sendAsync = function() {
            return contract.currentProvider.send.apply(
                contract.currentProvider, arguments
            );
        };
    }
    return contract;
}

export default fixTruffleContractCompatibilityIssue
