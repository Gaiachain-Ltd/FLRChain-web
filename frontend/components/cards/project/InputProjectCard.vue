<template>
  <DefaultCard :showOverlay="isSyncing">
    <v-layout column>
      <ProjectForm
        ref="projectForm"
        :project.sync="project"
        :readonly="readonly"
      ></ProjectForm>
      <DefaultText class="mb-3">{{ `Milestones & Tasks` }}</DefaultText>
      <v-layout :class="$vuetify.breakpoint.mdAndDown && 'wrap'">
        <v-flex :class="$vuetify.breakpoint.mdAndDown ? 'mb-6' : 'mr-6'">
          <v-layout column>
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
          ></InputBudgetCard>
        </v-layout>
      </v-layout>
    </v-layout>
  </DefaultCard>
</template>

<script>
import { SYNC } from "@/constants/project";

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