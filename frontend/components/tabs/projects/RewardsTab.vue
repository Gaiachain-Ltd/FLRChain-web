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
export default {
  props: {
    project: {},
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
};
</script>