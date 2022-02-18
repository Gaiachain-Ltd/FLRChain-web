<template>
  <v-layout column>
    <DetailsStewardsCard :project="project"></DetailsStewardsCard>
  </v-layout>
</template>

<script>
export default {
  props: {},
  components: {
    DetailsStewardsCard: () =>
      import("@/components/cards/project/DetailsStewardsCard"),
  },
};
</script>