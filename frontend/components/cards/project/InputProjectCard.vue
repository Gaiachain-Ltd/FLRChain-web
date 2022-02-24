<template>
  <DefaultCard>
    <v-layout column>
      <ProjectForm
        ref="projectForm"
        :project.sync="project"
        :readonly="readonly"
      ></ProjectForm>
      <DefaultText>{{ `Milestones & Tasks` }}</DefaultText>
      <v-layout wrap>
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
          <InputMilestonesCard
            :project.sync="project"
            :readonly="readonly"
          ></InputMilestonesCard>
          <InputBudgetCard
            :project.sync="project"
            :readonly="readonly"
            class="mt-6"
          ></InputBudgetCard>
        </v-layout>
      </v-layout>
    </v-layout>
  </DefaultCard>
</template>

<script>
export default {
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    InputMilestonesCard: () =>
      import("@/components/cards/project/InputMilestonesCard"),
    ProjectStructure: () =>
      import("@/components/widgets/projects/ProjectStructure"),
    ProjectFundDistribution: () =>
      import("@/components/widgets/projects/ProjectFundDistribution"),
    InputBudgetCard: () => import("@/components/cards/project/InputBudgetCard"),
  },
  methods: {
    validate() {
      return this.$refs.projectForm.validate();
    },
  },
};
</script>