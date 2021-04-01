<template>
  <DefaultAuthCard
    ref="card"
    title="Register"
    subtitle="Fill the form, make sure it's correct"
  >
    <v-layout column ma-0 slot="content">
      <v-form ref="form" v-model="isValid">
        <DefaultText
          class="mt-6"
          :size="12"
          :color="$vuetify.theme.themes.light.senary"
          >Select account type*</DefaultText
        >
        <v-radio-group row hide-details v-model="user.type">
          <v-radio label="Facilitator" :value="1"></v-radio>
          <v-radio label="Investor" :value="2"></v-radio>
        </v-radio-group>
        <v-layout row ma-0 mt-5 mx-0>
          <TextInput
            xs5
            label="First name*"
            placeholder="First name..."
            :text.sync="user.first_name"
            :rules="firstNameRules"
            required
          ></TextInput>
          <v-spacer></v-spacer>
          <TextInput
            xs5
            label="Last name*"
            placeholder="Last name..."
            :text.sync="user.last_name"
            :rules="lastNameRules"
            required
          ></TextInput>
        </v-layout>
        <v-flex shrink mx-0>
          <TextInput
            label="Email*"
            placeholder="Email..."
            :text.sync="user.email"
            :rules="emailRules"
            :error.sync="usedEmail"
            required
          ></TextInput>
        </v-flex>
        <v-layout row ma-0 mx-0>
          <TextInput
            xs5
            label="Password*"
            placeholder="Password..."
            :text.sync="user.password"
            :rules="passwordRules"
            :error.sync="passwordsNotTheSame"
            password
            required
          ></TextInput>
          <v-spacer></v-spacer>
          <TextInput
            xs5
            label="Re-password*"
            placeholder="Repeat password..."
            :text.sync="repassword"
            :rules="passwordRules"
            :error.sync="passwordsNotTheSame"
            password
            required
          ></TextInput>
        </v-layout>
        <v-flex ma-0 v-if="externalError">
          <DefaultText :size="12" class="error--text">{{
            externalError
          }}</DefaultText>
        </v-flex>
        <v-flex ma-0 mb-8>
          <BlockButton
            :disabled="!isValid || passwordsNotTheSame"
            @clicked="register"
            >Register</BlockButton
          >
        </v-flex>
      </v-form>
    </v-layout>
    <v-layout column align-center mb-2 slot="footer">
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
import ValidatorMixin from "@/validators";
import { mapActions } from 'vuex';

export default {
  mixins: [ValidatorMixin],
  data() {
    return {
      user: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        type: 1,
      },
      repassword: "",
      isValid: false,
      externalError: "",
      passwordsNotTheSame: false,
      usedEmail: false,
    };
  },
  watch: {
    user: {
      handler() {
        this.matchPasswords();
      },
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
    ...mapActions(["updateRegEmail"]),
    register() {
      if (this.isValid && !this.passwordsNotTheSame) {
        this.resetExternalErrors();
        this.$axios.post("register/", this.user)
        .then(
          () => {
            this.updateRegEmail(this.user.email);
            this.$router.push("/login");
          }
        )
        .catch(({ response }) => {
          if (response && response.data.email !== undefined) {
            this.usedEmail = true;
            this.externalError =
              "Email is already taken, please enter a different email address";
          } else {
            this.$refs.card.showErrorPopup();
          }
        });
      }
    },
    matchPasswords() {
      if (this.user.password !== this.repassword) {
        this.passwordsNotTheSame = true;
        this.externalError = "Password and re-password must be the same";
      } else if (this.passwordsNotTheSame) {
        this.resetExternalErrors();
      }
    },
    resetExternalErrors() {
      this.passwordsNotTheSame = false;
      this.usedEmail = false;
      this.externalError = "";
    },
  },
};
</script>