<template>
  <v-layout column mt-2 class="page-style">
    <ToolBar title="Dashboard"></ToolBar>
    <v-layout row ma-0 fill-height>
      <ProjectList
        class="mt-10 mr-6"
        title="My projects"
        :color="$vuetify.theme.themes.light.secondary"
      ></ProjectList>
      <ProjectList
        class="mt-10 ml-6"
        title="My active projects"
        :color="$vuetify.theme.themes.light.primary"
      ></ProjectList>
    </v-layout>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectList: () => import("@/components/lists/ProjectList"),
  },
};
</script>

<style scoped>
.page-style {
  max-height: calc(100vh - 32px) !important;
  overflow: hidden !important;
}
</style>