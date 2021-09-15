<template class="background-style">
  <v-flex mt-3>
    <v-tabs
      v-model="tabs"
      centered
      flat
      background-color="var(--v-accent-base)"
    >
      <v-tab>
        {{ firstTitle }}
      </v-tab>
      <v-tab>
        {{ secondTitle }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tabs">
      <v-tab-item>
        <v-card flat class="background-style">
          <v-flex pt-5>
          <ProjectList
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
            </v-flex>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat class="background-style">
          <v-flex pt-5>
          <ProjectList
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
          </v-flex>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-flex>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  data() {
    return {
      activeFilter: undefined,
      tabs: null,
    };
  },
  components: {
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
      return {investment__isnull: true};
    },
    secondTitle() {
      return this.isFacililator ? "My active projects" : "Donated projects";
    },
    secondQuery() {
      if (this.activeFilter === undefined) {
        return {investment__isnull: false};
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
.background-style {
  background-color: var(--v-accent-base) !important;
}
</style>
