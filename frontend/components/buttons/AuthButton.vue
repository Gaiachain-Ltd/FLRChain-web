<template>
  <v-btn
    @click.prevent="$emit('clicked')"
    class="auth-btn-style text-none elevation-0"
    block
    height="50"
    color="primary"
    :loading="loading"
    >{{ label }}</v-btn
  >
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
};
</script>

<style scoped>
.auth-btn-style {
  font-family: "open-sans" !important;
  font-size: 16px !important;
  font-weight: 600 !important;
}
</style>