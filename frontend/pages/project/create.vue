<template>
  <v-layout column fill-height mt-2>
    <ToolBar title="Create project"></ToolBar>
    <ProjectCard class="mt-6"></ProjectCard>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectCard: () => import("@/components/cards/project/ProjectCard"),
  },
};
</script>