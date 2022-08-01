<template>
  <v-layout column class="border-wrapper pa-3">
    <ProjectFundDistributionDelegate
      name="Tasks"
      :color="$vuetify.theme.themes.light.success"
      :value="totalRewards"
      :share="rewardsShare"
    ></ProjectFundDistributionDelegate>
    <ProjectFundDistributionDelegate
      name="Batch"
      color="blue"
      :value="totalBatch"
      :share="batchesShare"
    ></ProjectFundDistributionDelegate>
    <ProjectFundDistributionDelegate
      name="Facilitator"
      :color="$vuetify.theme.themes.light.primary"
      :value="totalFacAdmFunds"
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
import ProjectMixin from "@/mixins/ProjectMixin";

export default {
  mixins: [ProjectMixin],
  props: {
    project: {},
  },
  components: {
    ProjectFundDistributionDelegate: () =>
      import("@/components/delegates/projects/ProjectFundDistributionDelegate"),
  },
};
</script>

<style scoped>
.share {
  height: 14px;
}
.chart {
  border-radius: 10px;
  background-color: #dce0e7;
  overflow: hidden;
}
</style>