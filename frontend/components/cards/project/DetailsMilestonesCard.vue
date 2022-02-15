<template>
  <DefaultCardWithTitle>
    <DefaultText :color="$vuetify.theme.themes.light.primary" bold>{{
      `Milestones & Tasks`
    }}</DefaultText>
    <v-layout
      mt-3
      column
      v-for="(milestone, milestoneIndex) in project.milestones"
      :key="milestone.id"
    >
      <v-divider v-if="milestoneIndex" class="mt-2 mb-3"></v-divider>
      <v-layout column my-2>
        <v-layout mb-2>
          <DefaultText :size="14" bold>{{
            `Milestone ${milestoneIndex + 1}`
          }}</DefaultText>
          <v-spacer></v-spacer
          ><DefaultText :size="14">{{ `${milestone.name}` }}</DefaultText>
        </v-layout>
        <v-layout>
          <DefaultText :size="14" bold>Rewards (tasks and batch):</DefaultText>
          <v-spacer></v-spacer
          ><DefaultText :size="14">{{
            `${rewards(milestone)} USDC`
          }}</DefaultText>
        </v-layout>
      </v-layout>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
  },
  methods: {
    rewards(milestone) {
      let reward = 0;
      milestone.tasks.forEach(
        (task) =>
          (reward =
            parseFloat(task.batch) +
            parseFloat(task.reward) * parseFloat(task.count))
      );
      return reward;
    },
  },
};
</script>