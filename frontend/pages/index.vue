<template>
  <v-layout column fill-height mt-2>
    <ToolBar title="Dashboard"></ToolBar>
    <v-spacer></v-spacer>
  </v-layout>
</template>

<script>
export default {
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
  },
};
</script>