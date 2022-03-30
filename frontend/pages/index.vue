<template>
  <v-layout column ma-0>
    <ToolBar title="Projects"> </ToolBar>
    <v-card class="search-wrapper" style="background-color: #fafafd">
      <v-layout justify-center align-center fill-height>
        <v-text-field
          v-model="search"
          solo
          flat
          class="search"
          background-color="transparent"
          placeholder="Click to search projects..."
          hide-details
          clearable
        >
          <DefaultSVGIcon
            slot="append"
            :size="16"
            :icon="require('@/assets/icons/search.svg')"
          >
          </DefaultSVGIcon>
        </v-text-field>
      </v-layout>
    </v-card>
    <v-layout column ma-6>
      <v-layout column ma-0 shrink>
        <ProjectGroup
          v-if="fundraisingVisible"
          class="mt-6"
          title="Fundraising"
          :projects="fundraisingProjects"
        ></ProjectGroup>
        <ProjectGroup
          v-if="activeVisible"
          class="mt-6"
          :title="isFacililator ? 'Active' : 'Investments'"
          :projects="activeProjects"
        ></ProjectGroup>
        <ProjectGroup
          v-if="closedVisible"
          class="mt-6"
          title="Closed"
          :projects="closedProjects"
        ></ProjectGroup>
        <v-spacer></v-spacer>
      </v-layout>
      <v-spacer></v-spacer>
    </v-layout>
  </v-layout>
</template>

<script>
import _ from "lodash";
import { STATUS } from "@/constants/project";
import { mapGetters } from "vuex";

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
      search: null,
    };
  },
  watch: {
    search() {
      this.$fetch();
    },
  },
  computed: {
    ...mapGetters(["isFacililator"]),
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
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
  async fetch() {
    this.projects = await this.$axios
      .get("projects/", {
        params: {
          status: this.status !== -1 ? this.status : undefined,
          search: !!this.search ? this.search : undefined,
          nodetails: true
        },
      })
      .then((reply) => reply.data.results);
  },
};
</script>

<style scoped>
.search-wrapper {
  border-radius: 0px !important;
  background-color: var(--v-accent-base) !important;
  min-height: 70px;
}
.search {
  max-width: 235px;
}
.search ::v-deep input {
  text-align: center !important;
}
</style>