<template>
  <v-app-bar height="80px" app class="toolbar-style elevation-16">
    <v-layout row ma-0 align-center>
      <v-app-bar-nav-icon
        @click="toggleDrawer"
        class="hidden-lg-and-up"
      ></v-app-bar-nav-icon>
      <DefaultTitle>{{ title }}</DefaultTitle>
      <v-spacer></v-spacer>
      <v-flex shrink>
        <LogoutButton></LogoutButton>
      </v-flex>
    </v-layout>
  </v-app-bar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  props: {
    title: {
      type: String,
    },
  },
  components: {
    LogoutButton: () => import("@/components/buttons/LogoutButton"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
  },
  computed: {
    ...mapGetters(["getDrawerState"]),
  },
  methods: {
    ...mapActions(["updateDrawerState"]),
    toggleDrawer() {
      this.updateDrawerState(!this.getDrawerState);
    },
  },
};
</script>

<style scoped>
.toolbar-style {
  background-color: var(--v-accent-base) !important;
}
</style>