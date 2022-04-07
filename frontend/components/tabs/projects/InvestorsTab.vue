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
import SyncMixin from "@/mixins/SyncMixin";

export default {
  mixins: [SyncMixin],
  props: {
    project: {},
  },
  computed: {
    url() {
      return `projects/${this.project.id}/`;
    },
  },
  components: {
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
    DetailsInvestorsTableCard: () =>
      import("@/components/cards/project/DetailsInvestorsTableCard"),
  },
  async fetch() {
    this.refresh();
  },
};
</script>