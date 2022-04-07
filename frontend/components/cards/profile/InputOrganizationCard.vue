<template>
  <DefaultCard :title="title">
    <v-flex>
      <OrganizationForm
        ref="organizationForm"
        :organization.sync="organization"
      ></OrganizationForm>
    </v-flex>
  </DefaultCard>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    organization: {},
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    title() {
      return this.isFacililator
        ? "Facililator public profile"
        : "Investor public profile";
    },
  },
  components: {
    DefaultCard: () => import("@/components/cards/DefaultCard"),
    OrganizationForm: () =>
      import("@/components/forms/profile/OrganizationForm"),
  },
  methods: {
    validate() {
      return this.$refs.organizationForm.validate();
    }
  }
};
</script>