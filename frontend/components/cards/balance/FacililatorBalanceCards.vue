<template>
  <v-layout row shrink ma-0>
    <v-flex xs9 shrink>
      <BalanceCard
        :value="received"
        label="Project rewards in USDC"
      ></BalanceCard>
    </v-flex>
    <v-spacer></v-spacer>
    <v-flex xs2 shrink>
      <ProjectCounter></ProjectCounter>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      received: 0,
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
    ProjectCounter: () => import("@/components/cards/balance/ProjectCounter"),
  },
  async fetch() {
    const balanceInfo = await this.$axios
      .get("accounts/")
      .then((reply) => reply.data);
    this.received = balanceInfo.received;
  },
};
</script>