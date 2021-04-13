<template>
  <v-layout column mt-2>
    <ToolBar title="Project details"> </ToolBar>
    <v-layout row align-center ma-0 shrink mt-10 mb-5 >
      <DefaultTitle class="mr-3">{{ project.title }}</DefaultTitle>
      <ProjectStatusLabel :status="projectStatus"></ProjectStatusLabel>
      <v-spacer></v-spacer>
      <ActionButton
        v-if="!isFinished && isFacililator"
        class="white--text"
        :label="edit ? 'Save project' : 'Edit project'"
        :color="edit ? 'primary' : 'septenary'"
        @clicked="handleEdit"
      ></ActionButton>
    </v-layout>
    <v-layout row ma-0 shrink>
      <v-flex xs8 shrink>
        <v-layout column mr-3>
          <DetailsProjectCard
            v-if="!edit"
            class="mb-6"
            :project="project"
          ></DetailsProjectCard>
          <InputProjectCard
            v-else
            class="mb-6"
            :project.sync="project"
          ></InputProjectCard>
          <DetailsTasksCard
            v-if="!edit"
            class="mb-6"
            :tasks="project.tasks"
          ></DetailsTasksCard>
          <InputTasksCard
            v-else
            class="mb-6"
            :project.sync="project"
          ></InputTasksCard>
        </v-layout>
      </v-flex>
      <v-flex xs4 shrink>
        <v-layout column ml-3 xs4>
          <client-only v-if="project.investment" placeholder="Loading...">
            <DetailsInvestmentCard class="mb-6"></DetailsInvestmentCard>
          </client-only>
          <client-only v-if="project.investment" placeholder="Loading...">
            <DetailsInvestorsCard class="mb-6"></DetailsInvestorsCard>
          </client-only>
          <client-only v-if="isFacililator" placeholder="Loading...">
            <BeneficiariesCard class="mb-6"></BeneficiariesCard>
          </client-only>
          <client-only
            v-if="!isFacililator && !project.investment"
            placeholder="Loading..."
          >
            <InputInvestmentCard
              v-if="project.start"
              class="mb-6"
              @refresh="$fetch"
              :project="project"
            ></InputInvestmentCard>
          </client-only>
        </v-layout>
      </v-flex>
    </v-layout>
    <WorkHistoryCard v-if="project.investment"></WorkHistoryCard>
    <v-spacer></v-spacer>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
    <SuccessPopup
      v-if="successPopupVisible"
      :value.sync="successPopupVisible"
      text="Project has been saved successfully."
    ></SuccessPopup>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      errorPopupVisible: false,
      successPopupVisible: false,
      project: {},
      edit: false,
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
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
    DetailsInvestmentCard: () =>
      import("@/components/cards/project/DetailsInvestmentCard"),
    WorkHistoryCard: () => import("@/components/cards/project/WorkHistoryCard"),
    DetailsInvestorsCard: () =>
      import("@/components/cards/project/DetailsInvestorsCard"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputTasksCard: () => import("@/components/cards/project/InputTasksCard"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ProjectStatusLabel: () => import("@/components/texts/ProjectStatusLabel"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    isFinished() {
      return this.project.investment && this.project.investment.status === 0;
    },
    projectStatus() {
      if (this.project.investment) {
        if (this.isFinished) {
          return "Finished";
        } else {
          return "Ongoing";
        }
      } else {
        return "Waiting for investor";
      }
    },
  },
  methods: {
    handleEdit() {
      if (this.edit) {
        this.$axios
          .put(`projects/${this.$route.params.id}/`, this.project)
          .then((reply) => {
            this.project = reply.data;
            this.successPopupVisible = true;
          })
          .catch(() => (this.errorPopupVisible = true));
      }
      this.edit = !this.edit;
    },
  },
  async fetch() {
    this.project = await this.$axios
      .get(`projects/${this.$route.params.id}/`)
      .then((reply) => reply.data)
      .catch(() => (this.errorPopupVisible = true));
  },
};
</script>