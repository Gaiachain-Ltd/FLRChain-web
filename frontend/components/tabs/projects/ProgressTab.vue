<template>
  <v-layout column>
    <DetailsProgressTableCard :project="project"></DetailsProgressTableCard>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DetailsProgressTableCard: () =>
      import("@/components/cards/project/DetailsProgressTableCard"),
  },
};
</script>