<template>
  <v-card ma-0>
    <v-layout column ma-0 pa-6>
      <v-flex mb-6>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          title
        }}</DefaultText>
      </v-flex>
      <slot></slot>
    </v-layout>
  </v-card>
</template>
a
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