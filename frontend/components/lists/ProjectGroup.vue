<template>
  <v-layout column shrink>
    <v-layout>
      <DefaultText class="mb-3" size="20">{{ title }}</DefaultText>
      <v-badge class="badge" inline :content="projects.length" :color="counterColor"></v-badge>
      <v-spacer></v-spacer>
      <v-btn
        small
        icon
        style="background-color: white"
        class="elevation-16"
        @click.prevent="onClicked"
      >
        <v-img max-width="16" :src="collapseIcon" contain></v-img>
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
    counterColor() {
      switch (this.title) {
        case "Fundraising":
          return "#ff9123";
        case "Active":
        case "Investments":
          return "#00B854";
        case "Closed":
        case "Finished":
          return "#0075DC";
        default:
          return "";
      }
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

<style scoped>
.counter {
  color: white;
  border-radius: 10px;
  max-height: 20px;
  min-width: 20px;
  text-align: center;
  margin-top: 4px;
  margin-left: 4px;
}
.badge {
  margin-top: 3px;
}
</style>