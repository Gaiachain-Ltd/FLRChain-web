<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <TextInput
        label="Organization name"
        placeholder="Please enter organization name..."
        v-model="organization.name"
        :rules="[...maxLengthRules()]"
      ></TextInput>
      <Combobox
        label="Organization type"
        placeholder="Please select organization type..."
        v-model="organizationType"
        :items="organizationTypes"
      ></Combobox>
      <TextInput
        label="Website"
        placeholder="Please enter website..."
        v-model="organization.website"
        :rules="[...maxLengthRules()]"
      ></TextInput>
      <TextAreaInput
        label="Mission statement"
        placeholder="Please enter mission statement..."
        v-model="organization.statement"
        :rules="[...maxLengthRules(1023)]"
      ></TextAreaInput>
      <TextInput
        label="Name of principal contact"
        placeholder="Please enter name of principal contact..."
        v-model="organization.principal"
        :rules="[...maxLengthRules(511)]"
      ></TextInput>
      <TextInput
        label="Email"
        placeholder="Please enter your email address..."
        v-model="organization.email"
        :rules="[...emailRules]"
      ></TextInput>
      <TextInput
        label="Phone"
        placeholder="Please enter your phone number..."
        v-model="organization.phone"
        :rules="[...maxLengthRules(16)]"
      ></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";
import _ from "lodash";

export default {
  mixins: [ValidatorMixin],
  props: {
    organization: {},
  },
  data() {
    return {
      organizationTypes: [
        { text: "Profit", value: 0 },
        { text: "Nonprofit", value: 1 },
        { text: "Individual", value: 2 },
        { text: "Goverment", value: 3 },
        { text: "Other", value: 4 },
      ],
    };
  },
  computed: {
    organizationType: {
      get() {
        const index = _.findIndex(this.organizationTypes, [
          "value",
          this.organization.organization_type,
        ]);
        if (index !== -1) {
          return this.organizationTypes[index];
        } else {
          return null;
        }
      },
      set(value) {
        this.$set(this.organization, "organization_type", value.value);
      },
    },
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    Combobox: () => import("@/components/inputs/Combobox"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    }
  }
};
</script>