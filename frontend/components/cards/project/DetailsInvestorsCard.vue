<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText :color="$vuetify.theme.themes.light.primary" bold
        >Investors</DefaultText
      >
      <InvestmentDelegate
        v-for="investor in investors"
        :key="investor.id"
      ></InvestmentDelegate>
    </v-layout>
  </DefaultCard>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      investors: [],
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
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