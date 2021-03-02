<template>
  <v-btn style="auth-btn-style" block rounded height="50" color="primary">{{ label }}</v-btn>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
  },
};
</script>

<style scoped>
.auth-btn-style {
    font-family: 'open-sans' !important;
}
</style>