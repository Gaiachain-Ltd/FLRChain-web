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
      invested: 0,
    };
  },
  computed: {
    min() {
      return {
        label: "Raised",
        value: this.invested,
        share: parseFloat((this.invested / this.total) * 100).toFixed(2),
      };
    },
    max() {
      return {
        label: "Goal",
        value: this.total,
        share: 100,
      };
    },
  },
  components: {
    ProgressCard: () => import("@/components/cards/ProgressCard"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.invested = 0;
    await this.$axios
      .get(`projects/${this.project.id}/investors/`)
      .then((reply) =>
        reply.data
          .map((investor) => algosdk.microalgosToAlgos(investor.amount))
          .forEach((amount) => {
            this.invested += amount;
          })
      );
  },
};
</script>