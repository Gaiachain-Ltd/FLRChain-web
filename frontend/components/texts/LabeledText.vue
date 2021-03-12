<template>
  <v-layout column>
    <v-flex>
      <DefaultText :color="$vuetify.theme.themes.light.primary">{{
        label
      }}</DefaultText>
    </v-flex>
    <v-flex>
      <DefaultText :size="14">{{ text }}</DefaultText>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
    },
    text: {
      type: String,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>