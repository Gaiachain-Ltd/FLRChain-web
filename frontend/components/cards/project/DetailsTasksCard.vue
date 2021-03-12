<template>
  <v-card ma-0>
    <v-layout column ma-0 pa-6>
      <v-layout column ma-0 v-for="task in tasks" :key="task.id">
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
  },
};
</script>