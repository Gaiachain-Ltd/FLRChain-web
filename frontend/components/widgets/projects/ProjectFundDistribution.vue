<template>
  <v-layout column class="border-wrapper pa-3">
    <ProjectFundDistributionDelegate
      name="Tasks"
      :color="$vuetify.theme.themes.light.success"
      :value="rewards"
      :share="rewardsShare"
    ></ProjectFundDistributionDelegate>
    <ProjectFundDistributionDelegate
      name="Batch"
      color="blue"
      :value="batches"
      :share="batchesShare"
    ></ProjectFundDistributionDelegate>
    <ProjectFundDistributionDelegate
      name="Facilitator"
      :color="$vuetify.theme.themes.light.primary"
      :value="facAdmFunds"
      :share="facAdmFundsShare"
    ></ProjectFundDistributionDelegate>
    <v-layout class="chart mt-1">
      <div
        class="share"
        :style="{
          width: `${rewardsShare}%`,
          backgroundColor: $vuetify.theme.themes.light.success,
        }"
      ></div>
      <div
        class="share"
        :style="{
          width: `${batchesShare}%`,
          backgroundColor: 'blue',
        }"
      ></div>
      <div
        class="share"
        :style="{
          width: `${facAdmFundsShare}%`,
          backgroundColor: $vuetify.theme.themes.light.primary,
        }"
      ></div>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  computed: {
    rewards() {
      let rewards = 0;
      this.project.milestones.forEach((milestone) => {
        milestone.tasks.forEach((task) => {
          rewards += parseFloat(task.reward) * parseInt(task.count);
        });
      });
      return rewards;
    },
    batches() {
      let batches = 0;
      this.project.milestones.forEach((milestone) => {
        milestone.tasks.forEach((task) => {
          batches += parseFloat(task.batch);
        });
      });
      return batches;
    },
    facAdmFunds() {
      return this.project.fac_adm_funds
        ? parseFloat(this.project.fac_adm_funds).toFixed(2)
        : 0;
    },
    sum() {
      return this.rewards + this.batches + this.facAdmFunds;
    },
    rewardsShare() {
      if (!this.rewards) {
        return 0;
      }
      return (this.rewards * 100) / this.sum;
    },
    batchesShare() {
      if (!this.batches) {
        return 0;
      }
      return (this.batches * 100) / this.sum;
    },
    facAdmFundsShare() {
      if (!this.facAdmFunds) {
        return 0;
      }
      return (this.facAdmFunds * 100) / this.sum;
    },
  },
  components: {
    ProjectFundDistributionDelegate: () =>
      import("@/components/delegates/projects/ProjectFundDistributionDelegate"),
  },
};
</script>

<style scoped>
.share {
  height: 18px;
}
.chart {
  border-radius: 10px;
  background-color: #dce0e7;
  overflow: hidden;
}
</style>