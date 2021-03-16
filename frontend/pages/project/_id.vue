<template>
  <v-layout column mt-2>
    <ToolBar title="Project details"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">{{ project.title }}</DefaultTitle>
    <v-layout row ma-0>
      <v-flex xs8>
        <v-layout column mr-3>
          <DetailsProjectCard
            class="mb-6"
            :project="project"
          ></DetailsProjectCard>
          <DetailsTasksCard :tasks="project.tasks"></DetailsTasksCard>
        </v-layout>
      </v-flex>
      <v-flex xs4>
        <v-layout column ml-3 xs4>
          <client-only placeholder="Loading...">
            <BeneficiariesCard></BeneficiariesCard>
          </client-only>
        </v-layout>
      </v-flex>
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
    DetailsTasksCard: () =>
      import("@/components/cards/project/DetailsTasksCard"),
    BeneficiariesCard: () =>
      import("@/components/cards/project/BeneficiariesCard"),
  },
  async fetch() {
    this.project = await this.$axios
      .get(`projects/${this.$route.params.id}/`)
      .then((reply) => reply.data);
  },
};
</script>