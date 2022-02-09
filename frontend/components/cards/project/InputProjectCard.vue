<template>
  <DefaultCardWithTitle title="New project:">
    <v-layout column>
      <ProjectForm ref="projectForm" :project.sync="project"></ProjectForm>

      <DefaultText>{{ `Milestones & Tasks` }}</DefaultText>
      <v-layout>
        <v-flex xs2>
          <ProjectStructure :project="project" class="mr-6"></ProjectStructure>
        </v-flex>
        <v-layout column>
          <InputMilestonesCard :project.sync="project"></InputMilestonesCard>
        </v-layout>
      </v-layout>
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
    ProjectStructure: () =>
      import("@/components/widgets/projects/ProjectStructure"),
  },
  methods: {
    validate() {
      return this.$refs.projectForm.validate();
    },
  },
};
</script>