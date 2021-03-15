<template>
  <v-card ma-0>
    <v-layout column ma-0 pa-6>
      <v-flex mb-6>
        <DefaultText :color="$vuetify.theme.themes.light.primary"
          >Tasks:</DefaultText
        >
      </v-flex>
      <v-layout column ma-0 v-for="(task, index) in tasks" :key="task.id">
        <v-divider v-if="index" class="my-3"></v-divider>
        <DetailsTaskDelegate :task="task"></DetailsTaskDelegate>
      </v-layout>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    tasks: {},
  },
  components: {
    DetailsTaskDelegate: () =>
      import("@/components/delegates/DetailsTaskDelegate"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>