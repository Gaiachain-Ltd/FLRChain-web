<template>
  <v-layout column fill-height mt-2 style="width: 100%">
    <ToolBar title="Profile"></ToolBar>
    <InputOrganizationCard
      :organization.sync="organization"
    ></InputOrganizationCard>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      organization: {},
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InputOrganizationCard: () =>
      import("@/components/cards/profile/InputOrganizationCard"),
  },
  methods: {
    handleEdit() {
      this.$axios
        .patch("organization/", this.organization)
        .then((reply) => {
          console.log("Updated");
        })
        .catch((error) => {
          console.log("ERROR", error);
        });
    },
  },
  async fetch() {
    this.organization = await this.$axios
      .get("organization/")
      .then((reply) => reply.data)
      .catch((error) => {
        console.log("ERROR", error);
      });
  },
};
</script>