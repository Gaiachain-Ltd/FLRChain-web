<template>
  <DefaultCardWithTitle title="New project:">
      <v-flex>
        <ProjectForm ref="projectForm" :project.sync="project"></ProjectForm>
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
  },
  methods: {
    validate() {
      return this.$refs.projectForm.validate();
    }
  }
};
</script>