<template>
  <v-layout column>
    <DefaultText :size="14" :color="$vuetify.theme.themes.light.nonary">{{
      label
    }}</DefaultText>
    <v-layout row ma-0 align-center class="mt-3">
      <DefaultSVGIcon class="mr-2" :size="15" :icon="icon"></DefaultSVGIcon>
      <DefaultText class="mt-1" :size="12">
        {{ text }}
      </DefaultText>
    </v-layout>
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
    icon: {
      type: String,
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>