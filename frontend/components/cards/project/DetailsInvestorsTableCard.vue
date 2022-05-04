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
    </v-layout>
  </DefaultCard>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    InvestorsTable: () => import("@/components/tables/projects/InvestorsTable"),
  },
};
</script>