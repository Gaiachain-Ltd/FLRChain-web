<template>
  <v-layout column>
    <DefaultText
      v-if="title"
      class="mb-2"
      :color="$vuetify.theme.themes.light.primary"
      size="20"
      >{{ title }}</DefaultText
    >
    <v-card ma-0>
      <v-layout column ma-0 pa-6>
        <slot></slot>
      </v-layout>
      <v-overlay
        absolute
        :value="showOverlay"
        color="white"
        opacity="0.8"
      >
        <v-progress-circular
          indeterminate
          size="64"
          :color="$vuetify.theme.themes.light.primary"
        ></v-progress-circular>
      </v-overlay>
    </v-card>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    showOverlay: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>