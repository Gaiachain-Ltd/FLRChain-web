<template>
  <v-layout column shrink justify-center align-center class="wrapper-style">
    <DefaultText class="px-3" :size="12" color="white">{{ info }}</DefaultText>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      count: 0,
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    info() {
      return `${this.count} ${
        this.isFacililator
          ? this.count === 1
            ? "project"
            : "projects"
          : this.count === 1
          ? "project ready to invest"
          : "projects ready to invest"
      }`;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  async fetch() {
    this.count = await this.$axios
      .get("projects/", {
        params: {
          investment__isnull: true,
        },
      })
      .then((reply) => reply.data.count);
  },
};
</script>

<style scoped>
.wrapper-style {
  background-color: var(--v-secondary-base) !important;
  border-radius: 5px !important;
  height: 40px !important;
}
</style>