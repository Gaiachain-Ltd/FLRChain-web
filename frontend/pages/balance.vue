<template>
  <v-layout column>
    <ToolBar title="Balance"></ToolBar>
    <v-layout wrap shrink>
      <v-col v-if="isFacililator" class="ma-0 px-6 pb-3 pt-6" sm="12">
        <FacililatorBalanceCards></FacililatorBalanceCards>
      </v-col>
      <v-col v-else class="ma-0 px-6 pb-3 pt-6" sm="12">
        <InvestorBalanceCards></InvestorBalanceCards>
      </v-col>
      <v-col
        :class="['ma-0 pl-6 pt-3 pb-3 shrink', isFacililator ? 'pr-6' : 'pr-3']"
        :md="isFacililator ? 12 : 9"
        sm="12"
      >
        <MyWalletCard></MyWalletCard>
      </v-col>
      <v-col
        v-if="!isFacililator"
        class="ma-0 pr-6 pl-3 pt-3 pb-3 shrink"
        md="3"
        sm="12"
      >
        <TopUpCard></TopUpCard>
      </v-col>
      <v-col class="ma-0 px-6 pt-3 pb-6" sm="12">
        <TransactionHistoryCard></TransactionHistoryCard>
      </v-col>
    </v-layout>
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
