<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Rewards</DefaultText
      >
      <RewardsTable :project="project"></RewardsTable>
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
    RewardsTable: () => import("@/components/tables/projects/RewardsTable"),
  },
};
</script>