<template>
  <v-layout column mt-2 class="page-style">
    <ToolBar title="Dashboard"></ToolBar>
    <TabsMobile v-if="mobile"></TabsMobile>
    <TabsMdAndUp v-else></TabsMdAndUp>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {};
  },
  components: {
    TabsMobile: () => import("@/components/tabs/TabsMobile"),
    TabsMdAndUp: () => import("@/components/tabs/TabsMdAndUp"),
    ToolBar: () => import("@/components/toolbar/ToolBar"),
  },
  computed: {
    mobile() {
      return this.$vuetify.breakpoint.smAndDown
    },
  },
};
</script>

<style scoped>
.page-style {
  max-height: calc(100vh - 32px) !important;
  overflow: hidden !important;
}
</style>
