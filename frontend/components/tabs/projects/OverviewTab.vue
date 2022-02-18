<template>
  <v-layout column>
    <FundraisingProgressCard
      class="mb-6"
      :project="project"
    ></FundraisingProgressCard>
    <v-layout class="mb-6">
      <DetailsBlockchainCard :project="project"></DetailsBlockchainCard>
      <InputInvestmentCard v-if="project.status == 1" :project="project"></InputInvestmentCard>
    </v-layout>
    <InputProjectCard class="mb-6" :project.sync="project"></InputProjectCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DetailsBlockchainCard: () =>
      import("@/components/cards/project/DetailsBlockchainCard"),
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
  },
};
</script>