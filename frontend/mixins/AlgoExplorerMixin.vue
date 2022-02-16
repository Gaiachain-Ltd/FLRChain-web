<script>
export default {
  methods: {
    openExplorerTransactionLink(transactionId) {
      window.open(
        `https://testnet.algoexplorer.io/tx/${transactionId}`,
        "_blank"
      );
    },
    openExplorerApplicationLink(applicationId) {
      window.open(
        `https://testnet.algoexplorer.io/application/${applicationId}`,
        "_blank"
      );
    },
    openExplorerAddressLink(address) {
      window.open(
        `https://testnet.algoexplorer.io/address/${address}`,
        "_blank"
      );
    },
  },
};
</script>