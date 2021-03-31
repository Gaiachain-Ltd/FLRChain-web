<template>
  <DefaultCardWithTitle title="Investors:">
    <v-layout column>
      <InvestmentDelegate v-if="investment" :investment="investment"></InvestmentDelegate>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      investment: null,
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    InvestmentDelegate: () =>
      import("@/components/delegates/InvestmentDelegate"),
  },
  async fetch() {
    this.investment = await this.$axios
      .get(`projects/${this.$route.params.id}/investments/`)
      .then((reply) => reply.data);
  },
};
</script>