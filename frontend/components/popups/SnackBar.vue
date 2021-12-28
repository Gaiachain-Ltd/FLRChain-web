<template>
  <v-flex @click.stop="snackBarVisible = false">
    <v-snackbar
      class="snackbar-style elevation-20"
      bottom
      v-model="snackBarVisible"
      :timeout="timeout"
      color="white"
    >
      <v-layout justify-center align-center fill-height full-width>
        <DefaultText :color="color" size="20">{{ message }}</DefaultText>
        <DefaultSVGIcon
          class="ml-3 mb-1"
          :icon="icon"
          :size="40"
        ></DefaultSVGIcon>
      </v-layout>
    </v-snackbar>
  </v-flex>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    timeout: {
      type: Number,
      default: 2000,
    },
    message: {
      type: String,
      default: "Test",
    },
    positive: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    snackBarVisible: {
      get() {
        return this.visible;
      },
      set(value) {
        this.$emit("update:visible", value);
      },
    },
    icon() {
      if (this.positive) {
        return require("@/assets/popup/snackbar_success.svg");
      } else {
        return require("@/assets/popup/snackbar_error.svg");
      }
    },
    color() {
      if (this.positive) {
        return this.$vuetify.theme.themes.light.success;
      } else {
        return this.$vuetify.theme.themes.light.error;
      }
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>

<style scoped>
.snackbar-style ::v-deep .v-snack__wrapper {
  max-width: 100% !important;
  width: 100% !important;
  height: 120px !important;
  border: 0.5px lightgray solid !important;
}
</style>