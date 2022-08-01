<template>
  <v-layout column>
    <DetailsStewardsTableCard :project="project"></DetailsStewardsTableCard>
  </v-layout>
</template>

<script>
import SyncMixin from "@/mixins/SyncMixin";

export default {
  mixins: [SyncMixin],
  props: {
    project: {}
  },
  computed: {
    url() {
      return `projects/${this.project.id}/`;
    },
  },
  components: {
    DetailsStewardsTableCard: () =>
      import("@/components/cards/project/DetailsStewardsTableCard"),
  },
  async fetch() {
    this.refresh();
  },
};
</script>