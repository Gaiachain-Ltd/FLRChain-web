<template>
  <v-layout column>
    <DetailsRewardsTableCard :project="project"></DetailsRewardsTableCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DetailsRewardsTableCard: () =>
      import("@/components/cards/project/DetailsRewardsTableCard"),
  },
};
</script>