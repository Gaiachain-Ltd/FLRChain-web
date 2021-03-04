<template>
  <v-layout column>
    <v-layout row ma-0>
        <TextInput></TextInput>
        <DateInput></DateInput>
        <DateInput></DateInput>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
};
</script>