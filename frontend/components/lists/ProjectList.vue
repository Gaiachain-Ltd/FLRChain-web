<template>
  <v-layout column fill-height>
    <v-layout column fill-height>
      <DefaultText :size="24" :color="color">{{ title }}</DefaultText>
      <v-layout column ma-0 mt-6 class="list-style">
        <v-flex
          class="ma-0 mb-6 ml-1 mr-3"
          v-for="project in projects"
          :key="project.id"
          shrink
        >
          <slot name="delegate" v-bind:project="project">
            <DefaultProjectDelegate :project="project"></DefaultProjectDelegate>
          </slot>
        </v-flex>
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
    query: {
      type: Object,
      default: undefined,
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
      .get("projects/", { params: this.query })
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