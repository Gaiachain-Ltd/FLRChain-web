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
    <ActionBarCard @save="handleCreate" @cancel="handleCancel"></ActionBarCard>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
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
};
</script>

<style scoped>
.placeholder {
  width: 100% !important;
  height: 82px !important;
}
</style>