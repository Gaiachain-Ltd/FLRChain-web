<template>
  <v-layout column shrink>
    <v-layout>
      <DefaultText
        class="mb-3"
        size="20"
        :color="$vuetify.theme.themes.light.primary"
        >{{ title }}</DefaultText
      >
      <v-spacer></v-spacer>
      <v-btn
        small
        icon
        style="background-color: white"
        class="elevation-16"
        @click.prevent="onClicked"
      >
        <v-img
          max-width="16"
          :src="collapseIcon"
          contain
        ></v-img>
      </v-btn>
    </v-layout>
    <v-expand-transition>
      <v-row v-if="projects.length && !collapsed">
        <v-col xs6 v-for="project in projects" :key="project.id">
          <DefaultProjectDelegate :project="project"></DefaultProjectDelegate>
        </v-col>
      </v-row>
      <DefaultText v-else-if="!collapsed" class="mx-1"
        >No projects found.</DefaultText
      >
    </v-expand-transition>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: "Active projects",
    },
    projects: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      collapsed: false,
      upIcon: require("@/assets/icons/up.svg"),
      downIcon: require("@/assets/icons/down.svg"),
    };
  },
  computed: {
    collapseIcon() {
      return this.collapsed ? this.downIcon : this.upIcon;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
  methods: {
    onClicked() {
      this.collapsed = !this.collapsed;
    },
  },
};
</script>