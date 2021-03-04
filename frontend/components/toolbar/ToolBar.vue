<template>
  <v-layout row shrink ma-0 align-center>
    <div class="toolbar-title">{{ title }}</div>
    <v-spacer></v-spacer>
    <v-flex shrink>
      <LogoutButton></LogoutButton>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
  },
  components: {
    LogoutButton: () => import("@/components/buttons/LogoutButton"),
  },
};
</script>

<style scoped>
.toolbar-title {
  font-size: 28px !important;
  line-height: 40px !important;
  height: 40px;
  color: var(--v-quaternary-base);
}
</style>