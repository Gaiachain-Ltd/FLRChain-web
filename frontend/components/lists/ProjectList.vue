<template>
  <v-layout column fill-height>
    <v-layout row ma-0 shrink>
      <DefaultText :size="24" :color="$vuetify.theme.themes.light.primary">{{
        title
      }}</DefaultText>
      <v-spacer></v-spacer>
      <slot></slot>
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

const FUNDRAISING = 0;
const ACTIVE = 1;
const CLOSED = 2;

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
      return _.filter(this.projects, ['status', FUNDRAISING])
    },
    activeProjects() {
      return _.filter(this.projects, ['status', ACTIVE]);
    },
    closedProjects() {
      return _.filter(this.projects, ['status', CLOSED]);
    }
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
    ProjectGroup: () => import("@/components/lists/ProjectGroup"),
  },
  async fetch() {
    // TODO: Handle error!
    this.projects = await this.$axios
      .get("projects/", { params: this.query })
      .then((reply) => reply.data.results);
  },
};
</script>