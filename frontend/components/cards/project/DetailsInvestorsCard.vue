<template>
  <DefaultCard :showOverlay="showOverlay">
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Investors</DefaultText
      >
      <InvestorDelegate
        v-for="(investor, index) in investors"
        :key="index"
        :investor="investor"
      ></InvestorDelegate>
      <DefaultText v-if="!investors.length && !showOverlay"
        >No investors</DefaultText
      >
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
      showOverlay: true,
      investors: [],
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    InvestorDelegate: () =>
      import("@/components/delegates/projects/InvestorDelegate"),
  },
  async fetch() {
    this.investors = await this.$axios
      .get(`projects/${this.project.id}/investors/`)
      .then((reply) => reply.data);
    this.showOverlay = false;
  },
};
</script>