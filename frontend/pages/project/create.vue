<template>
  <v-layout column fill-height mt-2 style="width: 100%">
    <ToolBar title="Create project"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">New project</DefaultTitle>
    <InputProjectCard
      ref="inputProject"
      class="mb-5"
      :project.sync="project"
    ></InputProjectCard>
    <InputTasksCard ref="inputTasks" :project.sync="project"></InputTasksCard>
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
        tasks: [
          {
            action: "",
            reward: "0",
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
    ActionBarCard: () => import("@/components/cards/project/ActionBarCard"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    InfoPopup: () => import("@/components/popups/InfoPopup"),
  },
  computed: {
    blocked() {
      return this.$auth.user.opted_in;
    },
  },
  methods: {
    handleCreate() {
      if (
        this.$refs.inputProject.validate() &&
        this.$refs.inputTasks.validate()
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