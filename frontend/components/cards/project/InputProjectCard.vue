<template>
  <DefaultCardWithTitle title="New project:">
    <v-layout column>
      <ProjectForm ref="projectForm" :project.sync="project"></ProjectForm>
      <DefaultText>{{ `Milestones & Tasks` }}</DefaultText>
      <v-layout>
        <v-flex xs2>
          <v-layout column class="mr-6">
            <ProjectStructure :project="project"></ProjectStructure>
            <ProjectFundDistribution
              class="mt-3"
              :project="project"
            ></ProjectFundDistribution>
          </v-layout>
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
    ProjectFundDistribution: () =>
      import("@/components/widgets/projects/ProjectFundDistribution"),
  },
  methods: {
    validate() {
      return this.$refs.projectForm.validate();
    },
  },
};
</script>