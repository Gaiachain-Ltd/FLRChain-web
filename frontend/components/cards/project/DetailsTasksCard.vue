<template>
  <DefaultCardWithTitle title="Tasks:">
    <v-layout column ma-0 v-for="(task, index) in tasks" :key="task.id">
      <v-divider v-if="index" class="my-3"></v-divider>
      <DetailsTaskDelegate :task="task"></DetailsTaskDelegate>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  props: {
    tasks: {},
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    DetailsTaskDelegate: () =>
      import("@/components/delegates/DetailsTaskDelegate"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>