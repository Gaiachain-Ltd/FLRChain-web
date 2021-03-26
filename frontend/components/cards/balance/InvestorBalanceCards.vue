<template>
  <v-layout row full-width ma-0>
    <v-flex xs3>
      <BalanceCard :value="total" label="All USDC"></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs3>
      <BalanceCard :value="spent" label="Invested USDC"></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs3>
      <BalanceCard :value="balance" label="Balance USDC"></BalanceCard>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      total: 0,
      spent: 0,
      balance: 0,
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.total = balanceInfo.total;
    this.spent = balanceInfo.spent;
    this.balance = balanceInfo.balance;
  },
};
</script>