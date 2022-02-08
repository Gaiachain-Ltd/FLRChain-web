<template>
  <v-form ref="form">
    <v-layout column>
      <v-layout align-center>
        <v-flex md5 class="mr-3">
          <v-layout column>
            <TextInput
              label="Project title*"
              placeholder="Please enter project name..."
              v-model="project.title"
              :rules="requiredRules"
              required
            ></TextInput>
            <TextInput
              label="FLR Action"
              placeholder="Please enter project name..."
              v-model="project.title"
              :rules="requiredRules"
              required
            ></TextInput>
            <TextInput
              label="Fundraising duration"
              v-model="project.fundraising_duration"
              :rules="requiredRules"
              required
            ></TextInput>
            <v-layout>
              <DateInput
                label="Start of project*"
                :text.sync="project.start"
                :rules="[...requiredRules, ...dateRules]"
                required
              ></DateInput>
              <DateInput
                label="End of project*"
                :text.sync="project.end"
                :rules="[...requiredRules, ...dateRules]"
                required
              ></DateInput>
            </v-layout>
          </v-layout>
        </v-flex>
        <v-flex md7>
          <v-layout justify-center>
            <UploadButton></UploadButton>
          </v-layout>
        </v-flex>
      </v-layout>
      <TextAreaInput
        label="Description"
        placeholder="Please enter project description..."
        v-model="project.description"
      ></TextAreaInput>
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
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
    UploadButton: () => import("@/components/buttons/UploadButton"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>
