<template>
  <v-layout column fill-height mt-2>
    <ToolBar title="Create project"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">New project</DefaultTitle>
    <ProjectCard class="mb-5" :project.sync="project"></ProjectCard>
    <TasksCard :project.sync="project"></TasksCard>
    <v-spacer></v-spacer>
    <div class="placeholder"></div>
    <ActionBarCard @save="handleCreate" @cancel="handleCancel"></ActionBarCard>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
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
    ProjectCard: () => import("@/components/cards/project/ProjectCard"),
    TasksCard: () => import("@/components/cards/project/TasksCard"),
    ActionBarCard: () => import("@/components/cards/project/ActionBarCard"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
  },
  methods: {
    handleCreate() {
      // TODO: Handle errors!
      this.$axios.post("projects/", this.project).then(this.$router.push("/"));
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