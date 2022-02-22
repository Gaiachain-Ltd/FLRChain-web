<template>
  <v-layout column>
    <FundraisingProgressCard
      class="ma-3"
      :project="project"
    ></FundraisingProgressCard>
    <v-layout wrap>
      <v-col class="ma-0 pa-3" md="8" sm="12">
        <DetailsBlockchainCard :project="project"></DetailsBlockchainCard>
      </v-col>
      <v-col class="ma-0 pa-0" md="4" sm="12" v-if="project.status == 0">
        <InputInvestmentCard :project="project"></InputInvestmentCard>
      </v-col>
      <v-col
        :class="['ma-0 pa-3', project.status == 0 && 'order-md-2']"
        md="4"
        sm="12"
      >
        <DetailsStewardsCard :project="project"></DetailsStewardsCard>
      </v-col>
      <v-col class="ma-0 pa-3" :md="project.status != 0 ? 12 : 8" sm="12">
        <InputProjectCard :project.sync="project"></InputProjectCard>
      </v-col>
    </v-layout>
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
    DetailsStewardsCard: () =>
      import("@/components/cards/project/DetailsStewardsCard"),
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
  },
};
</script>