<template>
  <v-layout shrink class="justify-space-around">
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3>
      <BalanceCard :value="allocated" label="Allocated USDC"></BalanceCard>
    </v-layout>
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3>
      <BalanceCard :value="distributed" label="Distributed USDC"></BalanceCard>
    </v-layout>
    <v-layout xs12 sm5 md3 lg2 xl1 ma-3>
      <BalanceCard :value="balance" label="Balance USDC"></BalanceCard>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      allocated: 0,
      spent: 0,
      balance: 0,
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ButtonCard: () => import("@/components/cards/balance/ButtonCard"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.allocated = balanceInfo.allocated;
    this.distributed = balanceInfo.distributed;
    this.balance = balanceInfo.balance;
  },
};
</script>
