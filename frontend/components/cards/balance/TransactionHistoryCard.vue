<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Wallet History</DefaultText
      >
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
  </DefaultCard>
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
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
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
        const dt = this.$moment(element['created'], "YYYY-MM-DD")

        if (!date) {
          date = dt;
          addSeparatorWithDate = true;
        } else if (date.diff(dt, "days") != 0) {
          date = dt;
          addSeparatorWithDate = true;
        }

        processedTransactions.push({
          id: date + index,
          separator: true,
          date: addSeparatorWithDate
            ? date.format("YYYY-MM-DD")
            : undefined,
        });
        processedTransactions.push(element);
      }
      return processedTransactions;
    },
  },
  async fetch() {
    this.transactions = this.processTransactions(
      await this.$axios.get("transactions/").then((reply) => reply.data)
    );
  },
};
</script>