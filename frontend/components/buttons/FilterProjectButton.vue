<template>
  <v-btn
    class="filter-btn-style text-none elevation-0"
    height="40"
    color="#F1F5F8"
  >
    <v-layout row align-center px-2>
      <DefaultSVGIcon
        class="mr-2"
        v-if="activeProjects"
        :size="10"
        :icon="greenIcon"
      ></DefaultSVGIcon>
      <DefaultSVGIcon
        class="mr-2"
        v-if="inactiveProjects"
        :size="10"
        :icon="redIcon"
      ></DefaultSVGIcon>
      <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary">{{
        `${counter} ${label}`
      }}</DefaultText>
    </v-layout>
  </v-btn>
</template>

<script>
const FINISHED_PROJECT = 0;
const ONGOING_PROJECT = 1;

export default {
  props: {
    label: {
      type: String,
    },
    activeProjects: {
      type: Boolean,
      default: false,
    },
    inactiveProjects: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      greenIcon: require("@/assets/icons/active.svg"),
      redIcon: require("@/assets/icons/inactive.svg"),
      counter: 0,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
  async fetch() {
    this.counter = await this.$axios
      .get("projects/", {
        params: {
          investment__isnull: false,
          investment__status: this.activeProjects
            ? ONGOING_PROJECT
            : FINISHED_PROJECT,
        },
      })
      .then((reply) => reply.data.count);
  },
};
</script>

<style scoped>
.filter-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 16px !important;
  font-weight: 600 !important;
}
</style>