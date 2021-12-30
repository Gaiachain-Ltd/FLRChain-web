<template>
  <v-layout column ma-3>
    <ToolBar title="Projects"></ToolBar>
    <v-layout ma-0 align-center shrink>
      <DefaultText :size="24" :color="$vuetify.theme.themes.light.primary"
        >Your impact</DefaultText
      >
      <v-spacer></v-spacer>
      <ProjectsCounter
        :fundraising="fundraisingVisible ? fundraisingProjects.length : -1"
        :active="activeVisible ? activeProjects.length : -1"
        :closed="closedVisible ? closedProjects.length : -1"
      ></ProjectsCounter>
    </v-layout>
    <v-layout column ma-0 shrink>
      <ProjectGroup
        v-if="fundraisingVisible"
        class="mt-6"
        title="Fundraising projects"
        :projects="fundraisingProjects"
      ></ProjectGroup>
      <ProjectGroup
        v-if="activeVisible"
        class="mt-6"
        title="Active projects"
        :projects="activeProjects"
      ></ProjectGroup>
      <ProjectGroup
        v-if="closedVisible"
        class="mt-6"
        title="Closed projects"
        :projects="closedProjects"
      ></ProjectGroup>
      <v-spacer></v-spacer>
    </v-layout>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
import _ from "lodash";
import { STATUS } from "@/constants/project";

export default {
  props: {
    status: {
      type: Number,
      default: -1,
    },
  },
  data() {
    return {
      projects: [],
    };
  },
  computed: {
    fundraisingProjects() {
      return _.filter(this.projects, ["status", STATUS.FUNDRAISING]);
    },
    activeProjects() {
      return _.filter(this.projects, ["status", STATUS.ACTIVE]);
    },
    closedProjects() {
      return _.filter(this.projects, ["status", STATUS.CLOSED]);
    },
    fundraisingVisible() {
      return this.status === -1 || this.status == STATUS.FUNDRAISING;
    },
    activeVisible() {
      console.log("ACTIVE", this.status === -1 || this.status == STATUS.ACTIVE)
      return this.status === -1 || this.status == STATUS.ACTIVE;
    },
    closedVisible() {
      return this.status === -1 || this.status == STATUS.CLOSED;
    },
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
    ProjectGroup: () => import("@/components/lists/ProjectGroup"),
    ProjectsCounter: () =>
      import("@/components/widgets/projects/ProjectsCounter"),
  },
  async fetch() {
    this.projects = await this.$axios
      .get(
        "projects/",
        this.status !== -1 && { params: { status: this.status } }
      )
      .then((reply) => reply.data.results);
  },
};
</script>