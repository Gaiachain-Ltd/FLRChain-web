<template>
  <v-layout column>
    <DetailsStewardsTableCard :project="project"></DetailsStewardsTableCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {}
  },
  components: {
    DetailsStewardsTableCard: () =>
      import("@/components/cards/project/DetailsStewardsTableCard"),
  },
};
</script>