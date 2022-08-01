<template>
  <v-form ref="form" v-model="valid">
    <v-layout column>
      <TextInput
        label="Current password"
        placeholder="Please enter current password..."
        v-model="value.old_password"
        type="password"
        :rules="passwordRules"
        required
      ></TextInput>
      <TextInput
        label="New password"
        placeholder="Please enter new password..."
        type="password"
        v-model="value.new_password"
        :rules="passwordRules"
        :error.sync="passwordsNotTheSame"
        required
      ></TextInput>
      <TextInput
        label="Repeat new password"
        placeholder="Please repeat new password..."
        type="password"
        v-model="newPassword"
        :rules="passwordRules"
        :error.sync="passwordsNotTheSame"
        required
      ></TextInput>
      <v-flex mb-3 v-if="externalError">
        <DefaultText :size="12" class="error--text">{{
          externalError
        }}</DefaultText>
      </v-flex>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    value: {},
  },
  data() {
    return {
      valid: false,
      passwordsNotTheSame: false,
      externalError: "",
      newPassword: "",
    };
  },
  watch: {
    value: {
      new_password() {
        this.matchPasswords();
      },
    },
    newPassword() {
      this.matchPasswords();
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
  methods: {
    matchPasswords() {
      if (this.value.new_password !== this.newPassword) {
        this.passwordsNotTheSame = true;
        this.externalError =
          "Fields password and repeat password must be equal";
        return false;
      } else {
        this.passwordsNotTheSame = false;
        this.externalError = "";
        return true;
      }
    },
    isValid() {
        return this.valid && this.matchPasswords();
    }
  },
};
</script>