<template>
  <DefaultCard :showOverlay="isSyncing">
    <v-layout column>
      <ProjectForm
        ref="projectForm"
        :project.sync="project"
        :readonly="readonly"
      ></ProjectForm>
      <DefaultText>{{ `Milestones & Tasks` }}</DefaultText>
      <v-layout wrap>
        <v-flex xs3>
          <v-layout column class="mr-6">
            <ProjectStructure :project="project"></ProjectStructure>
            <ProjectFundDistribution
              class="mt-6"
              :project="project"
            ></ProjectFundDistribution>
          </v-layout>
        </v-flex>
        <v-layout column>
          <InputActionsCard
            :project.sync="project"
            :readonly="readonly"
          ></InputActionsCard>
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
import { SYNC, STATUS } from "@/constants/project";

export default {
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isSyncing() {
      return this.project.sync == SYNC.TO_SYNC;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    InputActionsCard: () =>
      import("@/components/cards/project/InputActionsCard"),
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