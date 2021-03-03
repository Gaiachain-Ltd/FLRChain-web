<template>
  <DefaultAuthCard title="Forgot password" subtitle="Please enter email">
    <v-layout column slot="content">
      <v-layout column mt-8>
        <TextInput placeholder="Please enter your email..."></TextInput>
      </v-layout>
      <v-flex mb-8>
        <AuthButton label="Remind password"></AuthButton>
      </v-flex>
    </v-layout>
    <v-layout column align-center mb-2 slot="footer">
      <DefaultText>You do not have account?</DefaultText>
      <DefaultText
        @clicked="$router.push('/register')"
        clickable
        :color="$vuetify.theme.themes.light.primary"
        >Register</DefaultText
      >
      <DefaultText class="mt-2">Have account already?</DefaultText>
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