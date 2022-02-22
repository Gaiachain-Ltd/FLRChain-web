<template>
  <v-layout column>
    <ToolBar title="Project details"></ToolBar>
    <v-layout column shrink>
      <v-card elevation-16 tile style="z-index: 1">
        <v-tabs v-model="currentProjectId" :height="80" centered hide-slider>
          <v-tab
            v-for="project in projects"
            :key="project.id"
            :value="`${project.id}`"
            active-class="active-project-tab"
            class="text-none inactive-project-tab"
            >{{ project.title }}
          </v-tab>
        </v-tabs>
      </v-card>
      <v-tabs-items
        mt-2
        v-model="currentProjectId"
        style="background-color: transparent"
      >
        <v-tab-item v-for="project in projects" :key="project.id">
          <v-card tile elevation-16>
            <v-tabs centered v-model="currentTab" :height="60">
              <v-tab
                v-for="tab in tabs"
                :key="tab.name"
                active-class="active-section-tab"
                class="text-none inactive-section-tab"
                >{{ tab.name }}</v-tab
              >
            </v-tabs>
          </v-card>
          <v-layout>
            <v-tabs-items
              v-model="currentTab"
              style="width: 100%; background-color: transparent"
            >
              <v-tab-item v-for="tab in tabs" :key="tab.name">
                <component
                  class="ma-3"
                  v-if="currentProject"
                  :project="currentProject"
                  :is="tab.component"
                ></component>
              </v-tab-item>
            </v-tabs-items>
          </v-layout>
        </v-tab-item>
      </v-tabs-items>
    </v-layout>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { Utility } from "@/utils/project";
import _ from "lodash";

export default {
  data() {
    return {
      projects: [],
      currentTab: 0,
      currentStatus: null,
    };
  },
  computed: {
    ...mapGetters(["getDetailsProjectId", "isFacililator"]),
    currentProjectId: {
      get() {
        const index = _.findIndex(this.projects, [
          "id",
          this.getDetailsProjectId,
        ]);
        return index !== -1 ? index : 0;
      },
      set(value) {
        if (this.projects.length) {
          this.updateDetailsProjectId(this.projects[value].id);
        }
      },
    },
    currentProject() {
      const index = _.findIndex(this.projects, [
        "id",
        this.getDetailsProjectId,
      ]);
      return index !== -1 ? this.projects[index] : null;
    },
    tabs() {
      return [
        {
          name: "Overview",
          component: "OverviewTab",
          visible: true,
        },
        {
          name: "Stewards",
          component: "StewardsTab",
          visible: this.isFacililator,
        },
        {
          name: "Rewards",
          visible: true,
        },
        {
          name: "Progress",
          visible: true,
        },
        {
          name: "Investors",
          component: "InvestorsTab",
          visible: true,
        },
      ].filter((tab) => tab.visible);
    },
  },
  methods: {
    ...mapActions(["updateDetailsProjectId"]),
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    OverviewTab: () => import("@/components/tabs/projects/OverviewTab"),
    InvestorsTab: () => import("@/components/tabs/projects/InvestorsTab"),
    StewardsTab: () => import("@/components/tabs/projects/StewardsTab")
  },
  async fetch() {
    this.projects = await this.$axios
      .get("projects/", {
        params: {
          status: Utility.statusValueByName(this.$route.params.status),
        },
      })
      .then((reply) => reply.data.results);
  },
};
</script>

<style scoped>
.inactive-project-tab {
  opacity: 0.6;
  word-spacing: normal;
}
.active-project-tab {
  background-color: var(--v-primary-base);
  border-radius: 10px;
  color: white !important;
  margin-top: 15px;
  padding-top: 5px;
  margin-bottom: 20px;
  opacity: 1;
  word-spacing: normal;
}
.inactive-section-tab {
  opacity: 0.6;
  word-spacing: normal;
}
.active-section-tab {
  color: var(--v-primary-base);
  opacity: 1;
  word-spacing: normal;
}
</style>