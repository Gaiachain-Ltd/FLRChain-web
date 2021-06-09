<template>
  <v-layout column>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
      label
    }}</DefaultText>
    <v-autocomplete
      class="text-field-style"
      :items="items"
      solo
      flat
      height="50"
      placeholder="Choose country..."
      :background-color="$vuetify.theme.themes.light.tertiary"
      v-model="internalText"
    ></v-autocomplete>
  </v-layout>
</template>

<script>
const countries = require("i18n-iso-countries");
countries.registerLocale(require("i18n-iso-countries/langs/en.json"));

export default {
  props: {
    label: {},
    text: {},
  },
  computed: {
    internalText: {
      get() {
        return this.text;
      },
      set(value) {
        this.$emit("update:text", value);
      },
    },
    items() {
      const list = countries.getNames("en", { select: "official" });
      return Object.keys(list).map((key) => ({ value: key, text: list[key] }));
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped lang="scss">
.text-field-style {
  border-radius: 7px !important;
}
</style>

<style lang="scss">
.text-field-style .v-text-field__details {
  padding: 0 !important;
}
</style>