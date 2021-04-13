<template>
  <v-flex class="wrapper" :style="{ backgroundColor: color }" shrink px-1>
    <DefaultText :size="12" color="white">{{ status }}</DefaultText>
  </v-flex>
</template>

<script>
export default {
  props: {
    status: {},
  },
  computed: {
    color() {
      switch (this.status) {
        case "Finished":
          return this.$vuetify.theme.themes.light.error;
        case "Ongoing":
          return this.$vuetify.theme.themes.light.primary;
        case "Waiting for investor":
          return this.$vuetify.theme.themes.light.septenary;
        default:
          return this.$vuetify.theme.themes.light.primary;
      }
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.wrapper {
  border-radius: 5px !important;
}
</style>