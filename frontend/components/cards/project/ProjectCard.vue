<template>
  <v-card mb-0>
    <v-card-text>
      <v-layout column ma-0 pa-4>
        <v-flex mb-3>
          <DefaultText :color="$vuetify.theme.themes.light.primary"
            >New project</DefaultText
          >
        </v-flex>
        <v-flex>
          <ProjectForm></ProjectForm>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>