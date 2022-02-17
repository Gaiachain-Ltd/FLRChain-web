<template>
  <ProgressCard :min="min" :max="max"></ProgressCard>
</template>

<script>
import algosdk from "algosdk";

export default {
  props: {
    project: {},
  },
  data() {
    return {
      invested: 0,
    };
  },
  computed: {
    total() {
      if (!this.project.milestones) {
        return 0;
      }
      let t = 0;
      this.project.milestones.forEach((milestone) =>
        milestone.tasks.forEach(
          (task) =>
            (t =
              parseFloat(task.batch) +
              parseFloat(task.reward) * parseFloat(task.count))
        )
      );
      return t;
    },
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