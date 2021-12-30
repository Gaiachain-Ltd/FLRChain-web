<template>
  <v-layout column fill-height>
    <ToolBar title="Projects"></ToolBar>
    <v-layout ma-0 align-center>
      <DefaultText :size="24" :color="$vuetify.theme.themes.light.primary"
        >Your impact</DefaultText
      >
      <v-spacer></v-spacer>
      <ProjectsCounter
        :fundraising="fundraisingProjects.length"
        :active="activeProjects.length"
        :closed="closedProjects.length"
      ></ProjectsCounter>
    </v-layout>
    <v-layout column ma-0>
      <ProjectGroup
        class="mt-6"
        title="Fundraising projects"
        :projects="fundraisingProjects"
      ></ProjectGroup>
      <ProjectGroup
        class="mt-6"
        title="Active projects"
        :projects="activeProjects"
      ></ProjectGroup>
      <ProjectGroup
        class="mt-6"
        title="Closed projects"
        :projects="closedProjects"
      ></ProjectGroup>
      <v-spacer></v-spacer>
    </v-layout>
  </v-layout>
</template>

<script>
import _ from "lodash";
import { STATUS } from "@/constants/project";

export default {
  props: {
    title: {
      type: String,
    },
    query: {
      type: Object,
      default: undefined,
    },
  },
  watch: {
    query() {
      this.$fetch();
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
    // TODO: Handle error!
    this.projects = await this.$axios
      .get("projects/")
      .then((reply) => reply.data.results);
  },
};
</script>