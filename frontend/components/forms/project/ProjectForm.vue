<template>
  <v-form ref="form">
    <v-layout column>
      <v-layout row ma-0>
        <v-flex xs12 sm12 md7 shrink>
          <TextInput
            label="Project title*"
            placeholder="Please enter project name..."
            v-model="project.title"
            :rules="requiredRules"
            required
          ></TextInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs12 sm5 md2 shrink>
          <DateInput
            label="Start of project*"
            :text.sync="project.start"
            :rules="[...requiredRules, ...dateRules]"
            required
          ></DateInput>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs12 sm5 md2 shrink>
          <DateInput
            label="End of project*"
            :text.sync="project.end"
            :rules="[...requiredRules, ...dateRules]"
            required
          ></DateInput>
        </v-flex>
      </v-layout>
      <v-layout row ma-0>
        <TextAreaInput
          label="Description"
          placeholder="Please enter project description..."
          v-model="project.description"
        ></TextAreaInput>
      </v-layout>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    project: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    }
  },
};
</script>
