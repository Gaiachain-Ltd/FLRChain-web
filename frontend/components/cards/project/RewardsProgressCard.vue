<template>
  <ProgressCard :min="min" :max="max"></ProgressCard>
</template>

<script>
import algosdk from "algosdk";
import ProjectMixin from "@/mixins/ProjectMixin";

export default {
  mixins: [ProjectMixin],
  props: {
    project: {},
  },
  data() {
    return {
      distributed: 0,
    };
  },
  computed: {
    totalShare() {
      return parseFloat((this.totalRewards + this.totalBatch).toFixed(2));
    },
    min() {
      return {
        label: "Distributed",
        value: this.distributed,
        share: parseFloat((this.distributed / this.totalShare) * 100).toFixed(2),
      };
    },
    max() {
      return {
        label: "Budget",
        value: this.totalShare,
        share: 100,
      };
    },
  },
  components: {
    ProgressCard: () => import("@/components/cards/ProgressCard"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.distributed = await this.$axios
      .get(`projects/${this.project.id}/distributed/`)
      .then((reply) => algosdk.microalgosToAlgos(reply.data.sum));
  },
};
</script>