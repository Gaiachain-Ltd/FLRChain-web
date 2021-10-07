<template>
  <DefaultAuthCard ref="card" title="Login" subtitle="Welcome back!">
    <v-layout column slot="content">
      <v-form ref="form">
        <v-layout column mt-8>
          <TextInput
            label="Email*"
            :text.sync="username"
            :rules="emailRules"
            :error.sync="wrongEmail"
            placeholder="Please enter your email..."
            required
          ></TextInput>
          <TextInput
            label="Password*"
            :text.sync="password"
            :rules="passwordRules"
            :error.sync="wrongPassword"
            placeholder="Please enter your password..."
            type="password"
            required
          ></TextInput>
        </v-layout>
        <v-layout row align-center mx-0 mb-3>
          <v-checkbox mb-0 label="Remember me"></v-checkbox>
          <v-spacer></v-spacer>
          <DefaultText
            @clicked="$router.push('/forgot')"
            :color="$vuetify.theme.themes.light.primary"
            clickable
            >Forgot password?</DefaultText
          >
        </v-layout>
        <v-flex ma-0 v-if="externalError">
          <DefaultText :size="12" class="error--text">{{
            externalError
          }}</DefaultText>
        </v-flex>
        <v-flex mb-8>
          <BlockButton :loading="loading" @clicked="logIn" type="submit">Log In</BlockButton>
        </v-flex>
      </v-form>
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
import ValidatorMixin from "@/validators";
import { mapGetters, mapActions } from "vuex";

export default {
  mixins: [ValidatorMixin],
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      externalError: "",
      wrongEmail: false,
      wrongPassword: false,
    };
  },
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  computed: {
    ...mapGetters(["regEmail"]),
  },
  methods: {
    ...mapActions(["updateRegEmail"]),
    logIn() {
      this.$auth
        .loginWith("local", {
          data: {
            username: this.username,
            password: this.password,
          },
        })
        .then(() => this.$router.push("/"))
        .catch(({ response }) => {
          if (response && response.data.non_field_errors) {
            this.wrongPassword = true;
            this.wrongEmail = true;
            this.externalError = "Provided credentials are incorrect";
          } else {
            this.$refs.card.showErrorPopup();
          }
        });
    },
  },
  mounted() {
    if (this.regEmail) {
      this.username = this.regEmail;
      this.updateRegEmail("");
      this.$refs.card.showSuccessPopup("Account has been created.");
    }
  },
};
</script>
