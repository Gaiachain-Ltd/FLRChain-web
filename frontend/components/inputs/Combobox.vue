<template>
  <v-layout column>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
      label
    }}</DefaultText>
    <v-combobox
      flat
      solo
      height="50"
      v-model="internalValue"
      :placeholder="placeholder"
      :items="items"
      :background-color="$vuetify.theme.themes.light.tertiary"
    ></v-combobox>
  </v-layout>
</template>

<script>
export default {
  props: {
    value: {},
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    error: {
      type: Boolean,
      default: false,
    },
    items: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    internalValue: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>