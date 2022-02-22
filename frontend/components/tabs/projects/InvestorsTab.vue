<template>
  <v-layout column>
    <FundraisingProgressCard
      class="mb-6"
      :project="project"
    ></FundraisingProgressCard>
    <DetailsInvestorsTableCard :project="project"></DetailsInvestorsTableCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
    DetailsInvestorsTableCard: () =>
      import("@/components/cards/project/DetailsInvestorsTableCard"),
  },
};
</script>