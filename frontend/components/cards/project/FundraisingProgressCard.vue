<template>
  <v-layout column>
    <v-layout>
        <v-layout v-for="(goal, index) in goals" :key="index">
            <DefaultText>{{ goal.label }}</DefaultText>
            <DefaultText>{{ goal.value }}</DefaultText>
            <DefaultText>{{ goal.share }}</DefaultText>
        </v-layout>
    </v-layout>
    <DefaultCard>
      <v-progress-linear :height="10"></v-progress-linear>
    </DefaultCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    points: {},
    value: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
  },
};
</script>