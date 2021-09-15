<template>
  <v-layout column ma-0>
    <ToolBar title="Balance"></ToolBar>
    <FacililatorBalanceCards
      v-if="isFacililator"
      class="mt-10"
    ></FacililatorBalanceCards>
    <InvestorBalanceCards v-else class="mt-10"></InvestorBalanceCards>
    <TransactionHistoryCard class="mt-10"></TransactionHistoryCard>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InvestorBalanceCards: () =>
      import("@/components/cards/balance/InvestorBalanceCards"),
    FacililatorBalanceCards: () =>
      import("@/components/cards/balance/FacililatorBalanceCards"),
    TransactionHistoryCard: () =>
      import("@/components/cards/balance/TransactionHistoryCard"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
  },
};
</script>
