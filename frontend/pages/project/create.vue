<template>
  <v-layout column fill-height ma-6>
    <ToolBar title="Create project"></ToolBar>
    <InputProjectCard
      ref="inputProject"
      class="mb-5"
      :project.sync="project"
    ></InputProjectCard>
    <v-spacer></v-spacer>
    <div class="placeholder"></div>
    <ActionBarCard
      :disabled="!$auth.user.opted_in"
      @save="handleCreate"
      @cancel="handleCancel"
    ></ActionBarCard>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
    <InfoPopup
      v-if="infoPopupVisible"
      :value.sync="infoPopupVisible"
      text="Your account is not active yet. Please try again later."
    ></InfoPopup>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      infoPopupVisible: false,
      errorPopupVisible: false,
      project: {
        title: "",
        description: "",
        start: this.$moment().format("YYYY-MM-DD"),
        end: this.$moment().format("YYYY-MM-DD"),
        milestones: [
          {
            name: "",
            tasks: [
              {
                action: "",
                reward: "0",
              },
            ],
          },
        ],
      },
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputTasksCard: () => import("@/components/cards/project/InputTasksCard"),
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    InfoPopup: () => import("@/components/popups/InfoPopup"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
  },
  computed: {
    blocked() {
      return this.$auth.user.opted_in;
    },
  },
  methods: {
    handleCreate() {
      if (
        this.$refs.inputProject.validate()
      ) {
        this.$axios
          .post("projects/", this.project)
          .then(() => this.$router.push("/"))
          .catch(() => (this.errorPopupVisible = true));
      }
    },
    handleCancel() {
      this.$router.back();
    },
  },
  async fetch() {
    if (!this.$auth.user.opted_in) {
      this.$auth.fetchUser().then(() => {
        if (!this.$auth.user.opted_in) {
          this.infoPopupVisible = true;
        }
      });
    }
  },
};
</script>

<style scoped>
.placeholder {
  width: 100% !important;
  height: 82px !important;
}
</style>