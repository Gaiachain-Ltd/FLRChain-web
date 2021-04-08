<template>
  <DefaultCardWithTitle title="History">
    <v-layout column ma-0>
      <template v-for="transaction in transactions">
        <v-layout column :key="transaction.id" ma-0>
          <v-layout
            row
            v-if="transaction.separator && transaction.date"
            align-center
            ma-0
          >
            <DefaultText size="14" class="mr-3">{{
              transaction.date
            }}</DefaultText>
            <v-divider></v-divider>
          </v-layout>
          <v-divider v-else-if="transaction.separator"></v-divider>
          <TransactionDelegate
            v-else
            class="my-6"
            :transaction="transaction"
          ></TransactionDelegate>
        </v-layout>
      </template>
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
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    TransactionDelegate: () =>
      import("@/components/delegates/TransactionDelegate"),
  },
  methods: {
    processTransactions(transactions) {
      let date = null;
      let processedTransactions = [];
      for (let index = 0; index < transactions.length; index++) {
        const element = transactions[index];
        let addSeparatorWithDate = false;
        if (!date) {
          date = element.created;
          addSeparatorWithDate = true;
        } else if (this.$moment(date).diff(element.created, "days") < 0) {
          date = element.created;
          addSeparatorWithDate = true;
        }

        processedTransactions.push({
          id: date + index,
          separator: true,
          date: addSeparatorWithDate
            ? this.$moment(date).format("YYYY-MM-DD")
            : undefined,
        });
        processedTransactions.push(element);
      }
      return processedTransactions;
    },
  },
  async fetch() {
    this.transactions = this.processTransactions(
      await this.$axios.get("transactions/").then((reply) => reply.data.results)
    );
  },
};
</script>