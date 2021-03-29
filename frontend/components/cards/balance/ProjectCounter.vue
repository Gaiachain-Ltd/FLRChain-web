<template>
  <BalanceCard :value="projects" label="All projects created"></BalanceCard>
</template>

<script>
export default {
  data() {
    return {
      projects: 0,
    };
  },
  components: {
    BalanceCard: () => import("@/components/cards/balance/BalanceCard"),
  },
  async fetch() {
    this.projects = await this.$axios
      .get("projects/")
      .then((reply) => reply.data.count);
  },
};
</script>