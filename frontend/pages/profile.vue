<template>
  <v-layout column fill-height ma-6>
    <ToolBar title="Profile"></ToolBar>
    <InputOrganizationCard
      ref="organizationForm"
      :organization.sync="organization"
    ></InputOrganizationCard>
    <ActionBarCard
      class="mb-6"
      :loading="loading"
      @cancel="$router.go(-1)"
      @save="handleEdit"
    >
      <ActionButton
        slot="extra"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.success} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.success} !important`"
        @click.prevent="showChangePasswordPopup = true"
        >Change password</ActionButton
      >
    </ActionBarCard>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
      :text="errorText"
    ></ErrorPopup>
    <ChangePasswordPopup
      v-if="showChangePasswordPopup"
      v-model="showChangePasswordPopup"
      @success="onSuccess"
      @error="onError"
    ></ChangePasswordPopup>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      organization: {},
      showChangePasswordPopup: false,
      loading: false,
      errorPopupVisible: false,
      errorText: "",
    };
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InputOrganizationCard: () =>
      import("@/components/cards/profile/InputOrganizationCard"),
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    ChangePasswordPopup: () =>
      import("@/components/popups/profile/ChangePasswordPopup"),
  },
  methods: {
    handleEdit() {
      if (this.$refs.organizationForm.validate()) {
        this.$axios
          .patch("organization/", this.organization)
          .then((reply) => {
            this.organization = reply.data;
            // this.onSuccess("Changes saved successfully!");
          })
          .catch(() => {
            this.showErrorPopup();
          });
      } else {
        this.showErrorPopup("Please correct fields marked on red.");
      }
    },
    showErrorPopup(text) {
      if (text) {
        this.errorText = text;
      } else {
        this.errorText = "Something went wrong. Please try again later.";
      }
      this.errorPopupVisible = true;
    },
  },
  async fetch() {
    this.organization = await this.$axios
      .get("organization/")
      .then((reply) => reply.data)
      .catch(() => {
        this.showErrorPopup();
      });
  },
};
</script>