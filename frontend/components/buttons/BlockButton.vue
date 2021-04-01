<template>
  <v-btn
    @click.prevent="$emit('clicked')"
    class="btn-style text-none elevation-0"
    block
    height="50"
    :color="color"
    :loading="loading"
    :disabled="disabled"
    ><slot></slot
  ></v-btn>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    color: {
      type: String,
      default: "primary",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 16px !important;
  font-weight: 600 !important;
}
</style>