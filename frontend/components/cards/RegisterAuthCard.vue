<template>
  <DefaultAuthCard
    title="Register"
    subtitle="Fill the form, make sure it's correct"
  >
    <v-layout column slot="content">
      <v-radio-group mt-6 row hide-details v-model="user.type">
        <v-radio label="Facilitator" :value="1"></v-radio>
        <v-radio label="Investor" :value="2"></v-radio>
      </v-radio-group>
      <v-layout row mt-5 mx-0>
        <TextInput
          xs5
          label="First name"
          placeholder="First name..."
          :text.sync="user.first_name"
        ></TextInput>
        <v-spacer></v-spacer>
        <TextInput
          xs5
          label="Last name"
          placeholder="Last name..."
          :text.sync="user.last_name"
        ></TextInput>
      </v-layout>
      <v-flex shrink mx-0>
        <TextInput
          label="Email"
          placeholder="Email..."
          :text.sync="user.email"
        ></TextInput>
      </v-flex>
      <v-layout row mx-0>
        <TextInput
          xs5
          label="Password"
          placeholder="Password..."
          :text.sync="user.password"
          password
        ></TextInput>
        <v-spacer></v-spacer>
        <TextInput
          xs5
          label="Re-password"
          placeholder="Repeat password..."
          :text.sync="repassword"
          password
        ></TextInput>
      </v-layout>
      <v-flex mb-8>
        <BlockButton @clicked="register">Register</BlockButton>
      </v-flex>
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
export default {
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
    };
  },
  components: {
    DefaultAuthCard: () => import("@/components/cards/DefaultAuthCard"),
    TextInput: () => import("@/components/inputs/TextInput"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    register() {
      this.$axios.post("register/", this.user)
    },
  },
};
</script>