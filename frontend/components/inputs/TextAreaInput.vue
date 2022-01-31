<template>
  <v-layout column>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
      label
    }}</DefaultText>
    <v-textarea
      class="text-field-style"
      :placeholder="placeholder"
      solo
      flat
      background-color="#f7f9fb"
      v-model="internalText"
      auto-grow
      :rows="4"
    ></v-textarea>
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
    password: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    internalText: {
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

<style scoped>
.text-field-style {
  border-radius: 7px !important;
}
</style>