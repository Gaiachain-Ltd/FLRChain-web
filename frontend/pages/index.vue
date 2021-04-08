<template>
  <v-layout column mt-2 class="page-style">
    <ToolBar title="Dashboard"></ToolBar>
    <v-layout row ma-0 fill-height>
      <ProjectList
        class="mt-10 mr-6"
        :title="firstTitle"
        :color="$vuetify.theme.themes.light.secondary"
        :query="firstQuery"
      >
        <template v-slot:delegate="{ project }">
          <DetailsProjectDelegate
            :project="project"
            :description="!isFacililator"
          ></DetailsProjectDelegate>
        </template>
        <ProjectsInfoLabel class="mr-3"></ProjectsInfoLabel>
      </ProjectList>
      <ProjectList
        class="mt-10 ml-6"
        :title="secondTitle"
        :color="$vuetify.theme.themes.light.primary"
        :query="secondQuery"
      >
        <template v-slot:delegate="{ project }">
          <InvestedProjectDelegate :project="project"></InvestedProjectDelegate>
        </template>
        <v-layout row ma-0 shrink align-center mr-3>
          <v-btn-toggle v-model="activeFilter">
            <v-flex shrink mr-3>
              <FilterProjectButton
                label="Ongoing"
                activeProjects
              ></FilterProjectButton>
            </v-flex>
            <v-flex shrink>
              <FilterProjectButton
                label="Finished"
                inactiveProjects
              ></FilterProjectButton>
            </v-flex>
          </v-btn-toggle>
        </v-layout>
      </ProjectList>
    </v-layout>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      activeFilter: undefined,
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    ProjectList: () => import("@/components/lists/ProjectList"),
    DetailsProjectDelegate: () =>
      import("@/components/delegates/DetailsProjectDelegate"),
    InvestedProjectDelegate: () =>
      import("@/components/delegates/InvestedProjectDelegate"),
    FilterProjectButton: () =>
      import("@/components/buttons/FilterProjectButton"),
    ProjectsInfoLabel: () => import("@/components/texts/ProjectsInfoLabel"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    firstTitle() {
      return this.isFacililator ? "My projects" : "Projects to invest";
    },
    firstQuery() {
      return { investment__isnull: true };
    },
    secondTitle() {
      return this.isFacililator ? "My active projects" : "Donated projects";
    },
    secondQuery() {
      if (this.activeFilter === undefined) {
        return { investment__isnull: false };
      } else {
        return {
          investment__isnull: false,
          investment__status: this.activeFilter === 0 ? 1 : 0,
        };
      }
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