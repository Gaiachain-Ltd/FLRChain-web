<template>
  <v-layout column shrink>
    <v-layout>
    <DefaultText class="mb-3" size="20" :color="$vuetify.theme.themes.light.primary">{{
      title
    }}</DefaultText>
    </v-layout>
    <v-row v-if="projects.length">
      <v-col xs6 v-for="project in projects" :key="project.id">
        <DefaultProjectDelegate :project="project"></DefaultProjectDelegate>
      </v-col>
    </v-row>
    <DefaultText v-else class="mx-1">No projects found.</DefaultText>
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
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
};
</script>