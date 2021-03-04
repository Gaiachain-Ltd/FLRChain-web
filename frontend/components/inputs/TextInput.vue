<template>
  <v-text-field
    class="text-field-style"
    :placeholder="placeholder"
    solo
    flat
    background-color="#f7f9fb"
    height="50"
    v-model="internalText"
    :type="password ? 'password' : 'text'"
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
    text: {
      type: String,
    },
    password: {
      type: Boolean,
      default: false
    }
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
  },
};
</script>

<style scoped>
.text-field-style {
  border-radius: 10px !important;
}
</style>