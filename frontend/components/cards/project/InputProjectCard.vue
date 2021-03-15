<template>
  <DefaultCardWithTitle title="New project:">
      <v-flex>
        <ProjectForm :project.sync="project"></ProjectForm>
      </v-flex>
    </DefaultCardWithTitle>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultCardWithTitle: () => import("@/components/cards/DefaultCardWithTitle"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>