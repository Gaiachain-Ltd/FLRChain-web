<template>
  <DefaultAuthCard
    ref="card"
    title="Change password"
    subtitle="Please enter new password"
  >
    <v-layout column slot="content">
      <v-form ref="form" v-model="isValid">
        <v-layout mt-8 mx-0>
          <TextInput
            xs5
            label="Password*"
            placeholder="Password..."
            v-model="password"
            :rules="passwordRules"
            :error.sync="passwordsNotTheSame"
            type="password"
            required
          ></TextInput>
          <v-spacer class="hidden-sm-and-down"></v-spacer>
          <TextInput
            xs5
            label="Re-password*"
            placeholder="Repeat password..."
            v-model="repassword"
            :rules="passwordRules"
            :error.sync="passwordsNotTheSame"
            type="password"
            required
          ></TextInput>
        </v-layout>
      </v-form>
      <v-flex ma-0 v-if="externalError">
        <DefaultText :size="12" class="error--text">{{
          externalError
        }}</DefaultText>
      </v-flex>
      <v-flex mb-8>
        <BlockButton @clicked="changePassword" type="submit" :loading="loading"
          >Change password</BlockButton
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
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  data() {
    return {
      isValid: false,
      password: "",
      repassword: "",
      passwordsNotTheSame: false,
      externalError: "",
      loading: false,
    };
  },
  watch: {
    password() {
      this.matchPasswords();
    },
    repassword() {
      this.matchPasswords();
    },
  },
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    matchPasswords() {
      if (this.password !== this.repassword) {
        this.passwordsNotTheSame = true;
        this.externalError = "Password and re-password must be the same";
      } else if (this.passwordsNotTheSame) {
        this.resetExternalErrors();
      }
    },
    changePassword() {
      if (this.isValid && !this.passwordsNotTheSame) {
        this.resetExternalErrors();
        this.loading = true;
        this.$axios
          .post("password_reset/confirm/", {
            password: this.password,
            token: this.$route.query.token,
          })
          .then((reply) => {
            this.loading = false;
            if (reply.data.status == "OK") {
              this.$refs.card.showSuccessPopup(
                "Your password has been changed."
              );
              setTimeout(() => this.$router.push("/login"), 2000);
            } else {
              this.$refs.card.showErrorPopup();
            }
          })
          .catch(() => {
            this.loading = false;
            this.$refs.card.showErrorPopup();
          });
      }
    },
    resetExternalErrors() {
      this.passwordsNotTheSame = false;
      this.externalError = "";
    },
  },
};
</script>