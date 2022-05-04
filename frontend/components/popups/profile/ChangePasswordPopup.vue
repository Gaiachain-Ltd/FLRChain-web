<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"></v-flex>
    <v-layout column slot="content" mt-6 mx-6>
      <DefaultText>Change password</DefaultText>
      <ChangePasswordForm
        ref="form"
        v-model="changePassword"
        class="mt-3"
      ></ChangePasswordForm>
    </v-layout>
    <v-layout slot="buttons" mb-6 mx-6>
      <v-spacer></v-spacer>
      <ActionButton
        class="mr-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="show = false"
        >Cancel</ActionButton
      >
      <ActionButton
        color="primary"
        @click.prevent="handleChangePassword"
        :loading="loading"
        >Change</ActionButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
    },
    text: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      loading: false,
      changePassword: {
        old_password: "",
        new_password: "",
      },
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    ChangePasswordForm: () =>
      import("@/components/forms/profile/ChangePasswordForm"),
  },
  methods: {
    handleChangePassword() {
      if (this.$refs.form.isValid()) {
        this.loading = true;
        this.$axios
          .post("change_password/", this.changePassword)
          .then((reply) => {
            if (reply.data.status == "OK") {
              this.$emit("success", "Password changed.");
              this.show = false;
            } else {
              this.$emit("Something has gone wrong.");
            }
          })
          .catch((error) => {
            console.log("ERROR", error);
            this.$emit("Something has gone wrong.");
          });
      }
    },
  },
};
</script>