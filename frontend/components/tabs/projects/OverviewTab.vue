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
      <v-col class="ma-0 pa-3" md="4" sm="12" v-if="!isFacililator">
        <InputInvestmentCard :project="project"></InputInvestmentCard>
      </v-col>
      <v-col
        :class="[
          'ma-0 pa-3',
          !isFacililator && project.status == 0 && 'order-md-2',
        ]"
        md="4"
        sm="12"
      >
        <DetailsStewardsCard :project="project"></DetailsStewardsCard>
      </v-col>
      <v-col class="ma-0 pa-3" :md="project.status != 0 ? 12 : 8" sm="12">
        <InputProjectCard
          :project.sync="project"
          :readonly="!isFacililator"
        ></InputProjectCard>
      </v-col>
    </v-layout>
    <ActionBarCard class="ma-3" @save="update" hideCancel></ActionBarCard>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    project: {},
  },
  computed: {
    ...mapGetters(["isFacililator"]),
  },
  components: {
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
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
  methods: {
    update() {
      this.$axios
        .put(`projects/${this.project.id}/`, this.project)
        .then((reply) => {
          console.log("SAVED!", reply);
        });
    },
  },
};
</script>