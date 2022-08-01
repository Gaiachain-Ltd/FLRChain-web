<template>
  <DefaultAuthCard
    ref="card"
    title="Forgot password"
    subtitle="Please enter email"
  >
    <v-layout column slot="content">
      <v-layout column mt-8>
        <TextInput
          v-model="email"
          placeholder="Please enter your email..."
        ></TextInput>
      </v-layout>
      <v-flex mb-8>
        <BlockButton @clicked="resetPassword" :loading="loading"
          >Reset password</BlockButton
        >
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
  data() {
    return {
      email: "",
      loading: false,
    };
  },
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    resetPassword() {
      this.loading = true;
      this.$axios
        .post("password_reset/", { email: this.email })
        .then((reply) => {
          this.loading = false;
          if (reply.data.status == "OK") {
            this.email = "";
            this.$refs.card.showSuccessPopup(
              "Reset link has been sent to your email."
            );
          } else {
            this.$refs.card.showErrorPopup();
          }
        })
        .catch(() => {
          this.loading = false;
          this.$refs.card.showErrorPopup();
        });
    },
  },
};
</script>