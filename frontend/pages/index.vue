<template>
  <v-layout column ma-3>
    <ToolBar title="Projects"></ToolBar>
    <ProjectList title="Your impact"></ProjectList>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {};
  },
  components: {
    TabsMobile: () => import("@/components/tabs/TabsMobile"),
    TabsMdAndUp: () => import("@/components/tabs/TabsMdAndUp"),
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectList: () => import("@/components/lists/ProjectList"),
  },
  computed: {
    mobile() {
      return this.$vuetify.breakpoint.smAndDown
    },
  },
};
</script>

<style scoped>
.page-style {
  max-height: calc(100vh - 32px) !important;
  overflow: hidden !important;
}
</style>
