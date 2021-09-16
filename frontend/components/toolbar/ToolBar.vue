<template>
  <v-layout row shrink ma-0 align-center>
    <v-app-bar-nav-icon @click="toggleDrawer" class="hidden-lg-and-up"></v-app-bar-nav-icon>
    <DefaultTitle>{{ title }}</DefaultTitle>
    <v-spacer></v-spacer>
    <v-flex shrink>
      <LogoutButton></LogoutButton>
    </v-flex>
  </v-layout>
</template>

<script>
import {mapGetters,mapActions} from 'vuex';
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
    ...mapGetters(['getDrawerState']),
  },
  methods: {
    ...mapActions(["updateDrawerState"]),
    toggleDrawer() {
      this.updateDrawerState(!this.getDrawerState);
    }
  }
};
</script>
