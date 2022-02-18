<template>
  <v-layout column>
    <FundraisingProgressCard
      class="mb-6"
      :project="project"
    ></FundraisingProgressCard>
    <DetailsInvestorsCard :project="project"></DetailsInvestorsCard>
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
    DetailsInvestorsCard: () =>
      import("@/components/cards/project/DetailsInvestorsCard"),
  },
};
</script>