<template>
  <BalanceCard :value="projects" label="Created" text="All your projects" currency="Projects"></BalanceCard>
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
      .get("projects/?nodetails=true")
      .then((reply) => reply.data.count);
  },
};
</script>