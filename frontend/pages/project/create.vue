<template>
  <v-layout column fill-height mt-2>
    <ToolBar title="Create project"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">New project</DefaultTitle>
    <ProjectCard></ProjectCard>
    <v-spacer></v-spacer>
    <div class="placeholder"></div>
    <ActionBarCard></ActionBarCard>
  </v-layout>
</template>

<script>
export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectCard: () => import("@/components/cards/project/ProjectCard"),
    ActionBarCard: () => import("@/components/cards/project/ActionBarCard"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
  },
};
</script>

<style scoped>
.placeholder {
  width: 100% !important;
  height: 82px !important;
}
</style>