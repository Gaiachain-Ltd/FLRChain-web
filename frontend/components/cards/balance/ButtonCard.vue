<template>
  <v-card style="height: 100%">
    <v-layout column align-center justify-center pa-3 style="height: 100%">
      <ActionButton :disabled="disabled" label="Add USDC" @clicked="$emit('clicked')"></ActionButton>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      default: 0,
    },
    label: {
      type: String,
      default: "",
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton")
  },
};
</script>