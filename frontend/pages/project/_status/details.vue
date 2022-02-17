<template>
  <v-layout column>
    <ToolBar title="Project details"></ToolBar>
    <v-layout column shrink>
      <v-tabs v-model="currentProjectId" fixed-tabs :height="100">
        <v-tab
          v-for="project in projects"
          :key="project.id"
          :value="`${project.id}`"
          >{{ project.title }}</v-tab
        >
      </v-tabs>
      <v-tabs-items
        v-model="currentProjectId"
        style="background-color: transparent"
      >
        <v-tab-item v-for="project in projects" :key="project.id">
          <v-layout shrink>
            <v-tabs centered v-model="currentTab">
              <v-tab v-for="tab in tabs" :key="tab.name">{{ tab.name }}</v-tab>
            </v-tabs>
          </v-layout>
          <v-layout>
            <v-tabs-items
              v-model="currentTab"
              style="width: 100%; background-color: transparent"
            >
              <v-tab-item>
                <OverviewCard
                  class="ma-6"
                  v-if="currentProject"
                  :project="currentProject"
                ></OverviewCard>
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
    ...mapGetters(["getDetailsProjectId"]),
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
          console.log("REPLACT", this.projects[value].id, value);
          this.updateDetailsProjectId(this.projects[value].id);
        }
      },
    },
    currentProject() {
      console.log("PROJECTSaa", this.projects);
      const index = _.findIndex(this.projects, [
        "id",
        this.getDetailsProjectId,
      ]);
      console.log("INDEX", index, this.$route.params.id);
      return index !== -1 ? this.projects[index] : null;
    },
    tabs() {
      return [
        {
          name: "Overview",
        },
        {
          name: "Rewards",
        },
        {
          name: "Progress",
        },
        {
          name: "Investors",
        },
      ];
    },
  },
  methods: {
    ...mapActions(["updateDetailsProjectId"]),
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    OverviewCard: () => import("@/components/cards/project/OverviewCard"),
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