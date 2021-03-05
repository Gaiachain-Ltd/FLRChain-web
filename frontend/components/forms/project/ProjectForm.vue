<template>
  <v-layout column>
    <v-layout row ma-0>
      <v-flex>
        <TextInput
          label="Project title"
          placeholder="Please enter project name..."
        ></TextInput>
      </v-flex>
      <v-flex mx-6>
        <DateInput label="Start of project"></DateInput>
      </v-flex>
      <v-flex>
        <DateInput label="End of project"></DateInput>
      </v-flex>
    </v-layout>
    <v-layout row ma-0>
      <TextAreaInput
        label="Description"
        placeholder="Please enter project description..."
      ></TextAreaInput>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
};
</script>