<script>
export default {
  methods: {
    openExplorerTransactionLink(transactionId) {
      window.open(
        `https://testnet.algoexplorer.io/tx/${transactionId}`,
        "_blank"
      );
    },
  },
};
</script>