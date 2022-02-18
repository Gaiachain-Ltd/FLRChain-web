<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Stewards</DefaultText
      >
      <StewardsTable :project="project"></StewardsTable>
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
    StewardsTable: () => import("@/components/tables/projects/StewardsTable"),
  },
};
</script>