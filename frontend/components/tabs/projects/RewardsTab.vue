<template>
  <v-layout column>
    <RewardsProgressCard
      ref="progress"
      class="mb-6"
      :project="project"
    ></RewardsProgressCard>
    <DetailsRewardsTableCard
      :project="project"
      @refresh="onRefresh"
    ></DetailsRewardsTableCard>
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
    RewardsProgressCard: () =>
      import("@/components/cards/project/RewardsProgressCard"),
    DetailsRewardsTableCard: () =>
      import("@/components/cards/project/DetailsRewardsTableCard"),
  },
  methods: {
    onRefresh() {
      this.$refs.progress.$fetch();
    },
  },
  async fetch() {
    this.refresh();
  },
};
</script>