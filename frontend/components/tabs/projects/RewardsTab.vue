<template>
  <v-layout column>
    <RewardsProgressCard class="mb-6" :project="project"></RewardsProgressCard>
    <DetailsRewardsTableCard :project="project"></DetailsRewardsTableCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    RewardsProgressCard: () =>
      import("@/components/cards/project/RewardsProgressCard"),
    DetailsRewardsTableCard: () =>
      import("@/components/cards/project/DetailsRewardsTableCard"),
  },
};
</script>