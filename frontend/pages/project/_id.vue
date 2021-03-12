<template>
  <v-layout column mt-2>
    <ToolBar title="Project details"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">{{ project.title }}</DefaultTitle>
    <v-layout row ma-0>
      <v-layout column>
        <DetailsProjectCard :project="project"></DetailsProjectCard>
      </v-layout>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      project: {},
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    DetailsProjectCard: () =>
      import("@/components/cards/project/DetailsProjectCard"),
  },
  async fetch() {
    this.project = await this.$axios
      .get(`projects/${this.$route.params.id}/`)
      .then((reply) => reply.data);
  },
};
</script>