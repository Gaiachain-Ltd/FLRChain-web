<template>
  <v-btn
    @click.prevent="$emit('clicked')"
    class="action-btn-style text-none elevation-0"
    height="50"
    :color="color"
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
  },
};
</script>

<style scoped>
.action-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  min-width: 250px !important;
}
</style>