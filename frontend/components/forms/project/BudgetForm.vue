<template>
  <v-layout column>
    <DefaultText class="mb-3" :color="$vuetify.theme.themes.light.primary"
      >Budget</DefaultText
    >
    <TextInput
      label="Facilitator administration funds"
      v-model="project.fac_adm_funds"
    ></TextInput>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>