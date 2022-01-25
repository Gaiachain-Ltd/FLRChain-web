<template>
  <DefaultCardWithTitle title="New project:">
    <v-layout column>
      <ProjectForm ref="projectForm" :project.sync="project"></ProjectForm>
      <DefaultText>{{ `Milestones & Tasks` }}</DefaultText>
      <InputMilestonesCard :project.sync="project"></InputMilestonesCard>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    InputMilestonesCard: () =>
      import("@/components/cards/project/InputMilestonesCard"),
  },
  methods: {
    validate() {
      return this.$refs.projectForm.validate();
    },
  },
};
</script>