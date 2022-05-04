<template>
  <v-app-bar height="80px" app class="toolbar-style elevation-16">
    <v-layout row ma-0 align-center>
      <v-app-bar-nav-icon
        @click="toggleDrawer"
        class="hidden-lg-and-up"
      ></v-app-bar-nav-icon>
      <v-flex
        shrink
        style="cursor: pointer"
        @click.prevent="() => $router.back()"
      >
        <DefaultSVGIcon
          v-if="showBackBtn"
          class="mb-1 mr-2"
          :icon="require('@/assets/toolbar/arrow-back.svg')"
        ></DefaultSVGIcon>
      </v-flex>
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
    showBackBtn: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    LogoutButton: () => import("@/components/buttons/LogoutButton"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
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