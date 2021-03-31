<template>
  <v-layout column ma-0>
    <v-layout row mb-3 ma-0>
      <v-flex>
        <DefaultText>Action:</DefaultText>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex shrink>
        <DefaultText>{{ task.action }}</DefaultText>
      </v-flex>
    </v-layout>
    <v-layout row ma-0 align-end>
      <v-flex>
        <DefaultText>Reward:</DefaultText>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex shrink>
        <DefaultText>{{ parseFloat(task.reward) }}</DefaultText>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
      task: {}
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>