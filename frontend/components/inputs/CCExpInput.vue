<template>
  <TextInput
    v-model="internalText"
    :label="label"
    :placeholder="placeholder"
    type="numeric"
    mask="##/####"
    :rules="[
      (v) => !!v || 'Field is required',
      (v) => /\d{2}\/\d{4}/.test(v) || 'Invalid format',
    ]"
  ></TextInput>
</template>

<script>
export default {
  props: {
    label: {},
    text: {},
    placeholder: {},
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
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>