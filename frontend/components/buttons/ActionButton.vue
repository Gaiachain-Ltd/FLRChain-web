<template>
  <v-btn
    @click.prevent="$emit('clicked')"
    class="action-btn-style text-none elevation-0"
    height="50"
    width="100%"
    max-width="400"
    :color="color"
    :disabled="disabled"
    >{{ label }}</v-btn
  >
</template>

<script>
export default {
  props: {
    label: {
      type: String,
    },
    color: {
      type: String,
      default: "primary",
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
};
</script>

<style scoped>
.action-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 16px !important;
  font-weight: 600 !important;
}
</style>
