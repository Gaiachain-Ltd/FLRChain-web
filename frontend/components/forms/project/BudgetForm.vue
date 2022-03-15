<template>
  <v-layout column>
    <DefaultText class="mb-3" :color="$vuetify.theme.themes.light.primary"
      >Budget</DefaultText
    >
    <TextInput
      label="Facilitator administration funds"
      v-model="project.fac_adm_funds"
      :readonly="readonly"
      :icon="icon"
    ></TextInput>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      icon: require("@/assets/icons/currency.svg"),
    }
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>