<template>
  <v-form ref="form">
    <v-layout column>
      <v-layout wrap align-center>
        <v-flex md5 class="pr-3">
          <v-layout column>
            <TextInput
              label="Project title*"
              placeholder="Please enter project name..."
              v-model="project.title"
              :rules="requiredRules"
              :readonly="readonly"
              required
            ></TextInput>
            <v-layout>
              <v-flex mr-3>
                <DateInput
                  label="Start of project*"
                  :text.sync="project.start"
                  :rules="[...requiredRules, ...dateRules]"
                  :readonly="readonly"
                  required
                ></DateInput>
              </v-flex>
              <v-flex ml-3>
                <DateInput
                  label="End of project*"
                  class="ml-3"
                  :text.sync="project.end"
                  :rules="[...requiredRules, ...dateRules]"
                  :readonly="readonly"
                  required
                ></DateInput>
              </v-flex>
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
        label="Summarize the project. What problem are you trying to solve and how?"
        placeholder="Please enter project description..."
        v-model="project.description"
        :readonly="readonly"
      ></TextAreaInput>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";
import _ from "lodash";

export default {
  mixins: [ValidatorMixin],
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      fundraisingPeriods: [
        { text: "1 month", value: 30 },
        { text: "2 months", value: 60 },
        { text: "3 months", value: 90 },
        { text: "4 months", value: 120 },
        { text: "5 months", value: 150 },
        { text: "6 months", value: 180 },
      ],
    };
  },
  computed: {
    fundraisingDuration: {
      get() {
        const index = _.findIndex(this.fundraisingPeriods, [
          "value",
          this.project.fundraising_duration,
        ]);
        if (index !== -1) {
          return this.fundraisingPeriods[index];
        } else {
          return null;
        }
      },
      set(value) {
        this.$set(this.project, "fundraising_duration", value.value);
      },
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DateInput: () => import("@/components/inputs/DateInput"),
    UploadButton: () => import("@/components/buttons/UploadButton"),
    Combobox: () => import("@/components/inputs/Combobox"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>
