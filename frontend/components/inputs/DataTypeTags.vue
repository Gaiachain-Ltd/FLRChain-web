<template>
  <v-layout column class="mb-4">
    <DefaultText class="mb-2" :size="12" :color="$vuetify.theme.themes.light.senary"
      >Type of data</DefaultText
    >
    <v-layout>
        <TagButton>Base line</TagButton>
      <TagButton creator>Add type</TagButton>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    TagButton: () => import("@/components/buttons/TagButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>