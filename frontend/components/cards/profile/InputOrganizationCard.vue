<template>
  <DefaultCard title="Investor public profile">
    <v-flex>
      <OrganizationForm
        ref="organizationForm"
        :organization.sync="organization"
      ></OrganizationForm>
    </v-flex>
  </DefaultCard>
</template>

<script>
export default {
  props: {
    organization: {},
  },
  components: {
    DefaultCard: () =>
      import("@/components/cards/DefaultCard"),
    OrganizationForm: () =>
      import("@/components/forms/profile/OrganizationForm"),
  },
};
</script>