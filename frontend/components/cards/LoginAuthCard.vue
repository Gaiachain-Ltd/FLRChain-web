<template>
  <DefaultAuthCard title="Login" subtitle="Welcome back!">
    <v-layout column slot="content">
      <v-layout column mt-8>
        <TextInput
          :text.sync="username"
          placeholder="Please enter your email..."
        ></TextInput>
        <TextInput
          :text.sync="password"
          placeholder="Please enter your password..."
        ></TextInput>
      </v-layout>
      <v-layout row align-center mx-0>
        <v-checkbox mb-0 label="Remember me"></v-checkbox>
        <v-spacer></v-spacer>
        <DefaultText
          @clicked="$router.push('/forgot')"
          clickable
          :color="$vuetify.theme.themes.light.primary"
          >Forgot password?</DefaultText
        >
      </v-layout>
      <v-flex mb-8 mt-6>
        <AuthButton
          label="Log In"
          :loading="loading"
          @clicked="logIn"
        ></AuthButton>
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
    </v-layout>
  </DefaultAuthCard>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      loading: false,
    };
  },
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    AuthButton: () => import("@/components/buttons/AuthButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    logIn() {
      this.$auth
        .loginWith("local", {
          data: {
            username: this.username,
            password: this.password,
          },
        })
        .then(() => this.$router.push('/'))
        .catch((error) => console.log("ERROR", error, error.response));
    },
  },
};
</script>