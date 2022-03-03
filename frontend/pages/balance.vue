<template>
  <v-layout wrap>
    <ToolBar title="Balance"></ToolBar>
    <!-- <FacililatorBalanceCards
      v-if="isFacililator"
      class="mt-10"
    ></FacililatorBalanceCards>
    <InvestorBalanceCards v-else class="mt-10"></InvestorBalanceCards> -->
    <v-col class="ma-0 pr-3 pl-6 pt-6 pb-3" md="9" shrink>
      <MyWalletCard></MyWalletCard>
    </v-col>
    <v-col class="ma-0 pr-6 pl-3 pt-6 pb-3" md="3">
      <TopUpCard></TopUpCard>
    </v-col>
    <v-col class="ma-0 px-6 pt-3 pb-6" sm="12">
      <TransactionHistoryCard></TransactionHistoryCard>
    </v-col>
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
    MyWalletCard: () => import("@/components/cards/balance/MyWalletCard"),
    TopUpCard: () => import("@/components/cards/balance/TopUpCard"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
  },
};
</script>
