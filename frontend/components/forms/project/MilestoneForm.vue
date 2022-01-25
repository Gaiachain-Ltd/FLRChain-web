<template>
  <v-form>
    <v-layout column>
      <TextInput label="Milestone name" :text.sync="milestone.name"></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  props: {
    value: {},
  },
  computed: {
    milestone: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>