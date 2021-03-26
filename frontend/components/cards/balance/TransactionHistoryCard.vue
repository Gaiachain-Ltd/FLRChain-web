<template>
  <DefaultCardWithTitle title="History">
    <v-layout column ma-0>
      <TransactionDelegate
        v-for="transaction in transactions"
        :key="transaction.id"
        :transaction="transaction"
      ></TransactionDelegate>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      transactions: [],
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    TransactionDelegate: () =>
      import("@/components/delegates/TransactionDelegate"),
  },
  async fetch() {
    this.transactions = await this.$axios
      .get("transactions/")
      .then((reply) => reply.data.results);
    console.log("TRANS", this.transactions);
  },
};
</script>