<template>
  <DefaultCardWithTitle title="Investor public profile:">
    <v-flex>
      <OrganizationForm
        ref="organizationForm"
        :organization.sync="organization"
      ></OrganizationForm>
    </v-flex>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  props: {
    organization: {},
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
    OrganizationForm: () =>
      import("@/components/forms/profile/OrganizationForm"),
  },
};
</script>