<template>
  <v-form>
    <v-layout column>
      <TextInput label="Milestone name"></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>