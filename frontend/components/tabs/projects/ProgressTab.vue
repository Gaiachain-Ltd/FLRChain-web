<template>
  <v-layout column>
    <DetailsProgressTableCard :project="project"></DetailsProgressTableCard>
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
    DetailsProgressTableCard: () =>
      import("@/components/cards/project/DetailsProgressTableCard"),
  },
  async fetch() {
    this.refresh();
  },
};
</script>