<template>
  <v-form ref="form">
    <v-layout column>
      <TextInput
        label="Organization name"
        placeholder="Please enter organization name..."
        v-model="organization.name"
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
      ></TextInput>
      <TextAreaInput
        label="Mission statement"
        placeholder="Please enter mission statement..."
        v-model="organization.statement"
      ></TextAreaInput>
      <TextInput
        label="Name of principal contact"
        placeholder="Please enter name of principal contact..."
        v-model="organization.principal"
      ></TextInput>
      <TextInput
        label="Email"
        placeholder="Please enter your email address..."
        v-model="organization.email"
      ></TextInput>
      <TextInput
        label="Phone"
        placeholder="Please enter your phone number..."
        v-model="organization.phone"
      ></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
import _ from "lodash";

export default {
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
};
</script>