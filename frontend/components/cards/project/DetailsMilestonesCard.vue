<template>
  <DefaultCard>
    <DefaultText :color="$vuetify.theme.themes.light.primary" bold>{{
      `Milestones & Tasks`
    }}</DefaultText>
  </DefaultCard>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
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