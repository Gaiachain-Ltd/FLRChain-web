<template>
  <v-layout column mt-2 class="page-style">
    <ToolBar title="Dashboard"></ToolBar>
    <v-layout row ma-0 fill-height>
      <ProjectList
        class="mt-10 mr-6"
        :title="firstTitle"
        :color="$vuetify.theme.themes.light.secondary"
        :query="firstQuery"
      ></ProjectList>
      <ProjectList
        class="mt-10 ml-6"
        :title="secondTitle"
        :color="$vuetify.theme.themes.light.primary"
        :query="secondQuery"
      ></ProjectList>
    </v-layout>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectList: () => import("@/components/lists/ProjectList"),
  },
  computed: {
    ...mapGetters(['isFacililator']),
    firstTitle() {
      return this.isFacililator ? 'My projects' : 'Projects to invest';
    },
    firstQuery() {
      return { investment__isnull: true };
    },
    secondTitle() {
      return this.isFacililator ? 'My active projects' : 'Donated projects';
    },
    secondQuery() {
      return { investment__isnull: false };
    }
  }
};
</script>

<style scoped>
.page-style {
  max-height: calc(100vh - 32px) !important;
  overflow: hidden !important;
}
</style>