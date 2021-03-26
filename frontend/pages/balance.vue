<template>
  <v-layout column ma-0>
    <ToolBar title="Balance"></ToolBar>
    <InvestorBalanceCards class="mt-10"></InvestorBalanceCards>
    <TransactionHistoryCard class="mt-10"></TransactionHistoryCard>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InvestorBalanceCards: () =>
      import("@/components/cards/balance/InvestorBalanceCards"),
    TransactionHistoryCard: () =>
      import("@/components/cards/balance/TransactionHistoryCard"),
  },
};
</script>