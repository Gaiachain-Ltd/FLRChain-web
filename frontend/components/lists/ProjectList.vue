<template>
  <v-layout column fill-height>
    <v-layout column fill-height>
      <DefaultText :size="24" :color="color">{{ title }}</DefaultText>
      <v-layout column mt-6 class="list-style">
        <DefaultProjectDelegate
          class="mb-6 ml-1 mr-3"
          v-for="project in projects"
          :key="project.id"
          :project="project"
        ></DefaultProjectDelegate>
        <v-flex>
          <div class="placeholder"></div>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    color: {
      type: String,
    },
  },
  data() {
    return {
      projects: [],
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
  async fetch() {
    // TODO: Handle error!
    this.projects = await this.$axios
      .get("projects/")
      .then((reply) => reply.data.results);
  },
};
</script>

<style scoped>
.list-style {
  max-height: calc(100% - 138px) !important;
  overflow: auto;
}
.placeholder {
  width: 100%;
  height: 12px;
}
</style>