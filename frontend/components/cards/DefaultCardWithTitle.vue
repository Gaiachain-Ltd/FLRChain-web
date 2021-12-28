<template>
  <v-layout column>
    <DefaultText class="mb-2" :color="$vuetify.theme.themes.light.primary" size="20">{{
      title
    }}</DefaultText>
    <v-card ma-0>
      <v-layout column ma-0 pa-6>
        <slot></slot>
      </v-layout>
    </v-card>
  </v-layout>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>