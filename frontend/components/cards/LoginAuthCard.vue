<template>
  <DefaultAuthCard title="Login" subtitle="Welcome back!">
    <v-layout column slot="content">
      <v-layout column mt-8>
        <TextInput placeholder="Please enter your email..."></TextInput>
        <TextInput placeholder="Please enter your password..."></TextInput>
      </v-layout>
      <v-layout row align-center mx-0>
        <v-checkbox label="Remember me"></v-checkbox>
        <v-spacer></v-spacer>
        <DefaultText
          @clicked="$router.push('/forgot')"
          clickable
          :color="$vuetify.theme.themes.light.primary"
          >Forgot password?</DefaultText
        >
      </v-layout>
      <v-flex mb-8 mt-6>
        <AuthButton label="Log In"></AuthButton>
      </v-flex>
    </v-layout>
    <v-layout column align-center slot="footer">
      <DefaultText>You do not have account?</DefaultText>
      <DefaultText
        @clicked="$router.push('/register')"
        clickable
        :color="$vuetify.theme.themes.light.primary"
        >Register</DefaultText
      >
    </v-layout>
  </DefaultAuthCard>
</template>

<script>
export default {
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    AuthButton: () => import("@/components/buttons/AuthButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>