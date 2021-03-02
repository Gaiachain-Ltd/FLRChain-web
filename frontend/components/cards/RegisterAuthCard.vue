<template>
  <DefaultAuthCard
    title="Register"
    subtitle="Fill the form, make sure it's correct"
  >
    <v-layout column slot="content">
      <v-layout row mt-8 mx-0>
        <TextInput xs5 placeholder="First name..."></TextInput>
        <v-spacer></v-spacer>
        <TextInput xs5 placeholder="Last name..."></TextInput>
      </v-layout>
      <v-flex shrink mx-0>
        <TextInput placeholder="Email..."></TextInput>
      </v-flex>
        <v-layout row mx-0>
        <TextInput xs5 placeholder="Password..."></TextInput>
        <v-spacer></v-spacer>
        <TextInput xs5 placeholder="Repeat password..."></TextInput>
      </v-layout>
      <v-flex mb-8>
        <AuthButton label="Register"></AuthButton>
      </v-flex>
    </v-layout>
    <v-layout column align-center slot="footer">
      <DefaultText>Have account already?</DefaultText>
      <DefaultText
        @clicked="$router.push('/login')"
        clickable
        :color="$vuetify.theme.themes.light.primary"
        >Log In</DefaultText
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