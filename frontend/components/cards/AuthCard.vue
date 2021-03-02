<template>
  <v-card min-width="500">
    <v-card-title>{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
    <v-card-text>
        <v-divider></v-divider>
        <v-layout column mt-8>
            <TextInput placeholder="Please enter your email..."></TextInput>
            <TextInput></TextInput>
        </v-layout>
        <v-flex mb-8>
            <AuthButton label="Login"></AuthButton>
        </v-flex>
        <v-divider></v-divider>
    </v-card-text>
    <v-card-action>
        <v-layout column align-center>
            <div>You don't have an account?</div>
            <div>Register</div>
        </v-layout>
    </v-card-action>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    subtitle: {
      type: String,
    },
  },
  components: {
      TextInput: () => import("@/components/inputs/TextInput"),
      AuthButton: () => import("@/components/buttons/AuthButton")
  }
};
</script>