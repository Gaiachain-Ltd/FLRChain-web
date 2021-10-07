<template>
  <v-layout row shrink ma-0 class="justify-space-around">
    <v-layout xs12 sm5 md4 lg3 xl3 ma-3 shrink>
      <BalanceCard
        :value="received"
        label="Project rewards in USDC"
      ></BalanceCard>
    </v-layout>
    <v-layout xs12 sm5 md4 lg3 xl3 ma-3 shrink>
      <ProjectCounter></ProjectCounter>
    </v-layout>
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
