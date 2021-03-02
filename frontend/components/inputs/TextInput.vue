<template>
  <v-text-field
    class="text-field-style"
    :placeholder="placeholder"
    solo
    flat
    background-color="#f7f9fb"
    height="50"
  ></v-text-field>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
  },
};
</script>

<style scoped>
.text-field-style {
  border-radius: 10px;
}
</style>