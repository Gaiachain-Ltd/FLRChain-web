<template>
  <v-form ref="form">
    <v-layout column>
      <TextInput
        label="Organization name"
        placeholder="Please enter organization name..."
        :text.sync="organization.name"
      ></TextInput>
      <TextInput
        label="Website"
        placeholder="Please enter website..."
        :text.sync="organization.website"
      ></TextInput>
      <TextAreaInput
        label="Mission statement"
        placeholder="Please enter mission statement..."
        :text.sync="organization.statement"
      ></TextAreaInput>
      <TextInput
        label="Name of principal contact"
        placeholder="Please enter name of principal contact..."
        :text.sync="organization.principal"
      ></TextInput>
      <TextInput
        label="Email"
        placeholder="Please enter your email address..."
        :text.sync="organization.email"
      ></TextInput>
      <TextInput
        label="Phone"
        placeholder="Please enter your phone number..."
        :text.sync="organization.phone"
      ></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  props: {
    organization: {},
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
  },
};
</script>