<template>
  <v-layout row class="delegate-style pa-2 pt-3" ma-0 align-center>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary">{{
      label
    }}</DefaultText>
    <v-spacer></v-spacer>
    <DefaultText
      class="ml-6"
      :size="12"
      :color="$vuetify.theme.themes.light.quinary"
      >{{ formattedValue }}</DefaultText
    >
  </v-layout>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
    },
    value: {
      type: String | Number,
    },
    usdc: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    formattedValue() {
      if (this.usdc) {
        return `${parseFloat(this.value)} USDC`;
      } else {
        return `${parseFloat(this.value)}`;
      }
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.delegate-style {
  border-radius: 5px !important;
  background-color: #f1f5f8 !important;
}
</style>