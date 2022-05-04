<template>
  <DefaultCard>
    <v-layout column>
      <DefaultText
        class="mb-3"
        :color="$vuetify.theme.themes.light.primary"
        bold
        >Data submitted by stewards</DefaultText
      >
      <ProgressTable :project="project"></ProgressTable>
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
    ProgressTable: () => import("@/components/tables/projects/ProgressTable"),
  },
};
</script>