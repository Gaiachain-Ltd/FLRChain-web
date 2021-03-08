<template>
  <v-layout column>
    <v-layout row ma-0>
      <v-flex>
        <TextInput
          label="Project title"
          placeholder="Please enter project name..."
          :text.sync="project.title"
        ></TextInput>
      </v-flex>
      <v-flex mx-6>
        <DateInput
          label="Start of project"
          :text.sync="project.start"
        ></DateInput>
      </v-flex>
      <v-flex>
        <DateInput label="End of project" :text.sync="project.end"></DateInput>
      </v-flex>
    </v-layout>
    <v-layout row ma-0>
      <TextAreaInput
        label="Description"
        placeholder="Please enter project description..."
        :text.sync="project.description"
      ></TextAreaInput>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
};
</script>