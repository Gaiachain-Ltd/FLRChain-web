<template>
  <v-layout column fill-height ma-3 style="width: 100%">
    <ToolBar title="Profile"></ToolBar>
    <InputOrganizationCard
      :organization.sync="organization"
    ></InputOrganizationCard>
    <ActionBarCard
      class="mb-6"
      :loading="loading"
      @cancel="$router.go(-1)"
      @save="handleEdit"
    ></ActionBarCard>
    <SuccessPopup :value.sync="showSuccessPopup" :text="message"></SuccessPopup>
    <ErrorPopup :value.sync="showErrorPopup" :text="message"></ErrorPopup>
  </v-layout>
</template>

<script>
import CRUDMixin from "@/mixins/CRUDMixin";

export default {
  mixins: [CRUDMixin],
  data() {
    return {
      organization: {},
      loading: false,
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InputOrganizationCard: () =>
      import("@/components/cards/profile/InputOrganizationCard"),
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
  },
  methods: {
    handleEdit() {
      this.beforeRequest();
      this.$axios
        .patch("organization/", this.organization)
        .then((reply) => {
          this.organization = reply.data;
          this.onSuccess();
        })
        .catch((error) => {
          this.onError("Something has gone wrong. Please try again later.");
        });
    },
  },
  async fetch() {
    this.organization = await this.$axios
      .get("organization/")
      .then((reply) => reply.data)
      .catch((error) => {
        this.onError("Something has gone wrong. Please try again later.")
      });
  },
};
</script>