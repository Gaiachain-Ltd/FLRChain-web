<template>
  <v-layout column>
    <DefaultText size="20" :color="$vuetify.theme.themes.light.primary">{{
      title
    }}</DefaultText>
    <v-row>
      <v-col xs6 v-for="project in projects" :key="project.id">
        <DefaultProjectDelegate :project="project"></DefaultProjectDelegate>
      </v-col>
    </v-row>
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
      type: String,
      default: () => [],
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
};
</script>