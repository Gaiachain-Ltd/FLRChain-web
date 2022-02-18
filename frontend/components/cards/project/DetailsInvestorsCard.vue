<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Investors</DefaultText
      >
      <InvestorsTable :project="project"></InvestorsTable>
      <!-- <InvestorDelegate
        v-for="(investor, index) in investors"
        :key="index"
        :investor="investor"
      ></InvestorDelegate>
      <DefaultText v-if="!investors.length && !showOverlay"
        >No investors</DefaultText
      > -->
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
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    InvestorDelegate: () =>
      import("@/components/delegates/projects/InvestorDelegate"),
    InvestorsTable: () => import("@/components/tables/projects/InvestorsTable")
  }
};
</script>