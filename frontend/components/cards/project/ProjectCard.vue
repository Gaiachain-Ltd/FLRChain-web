<template>
  <v-card mb-0>
    <v-layout column ma-0 pa-6>
      <v-flex mb-3>
        <DefaultText :color="$vuetify.theme.themes.light.primary"
          >New project</DefaultText
        >
      </v-flex>
      <v-flex>
        <ProjectForm :project.sync="project"></ProjectForm>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>