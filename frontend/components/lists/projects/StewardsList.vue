<template>
  <v-layout column>
    <v-layout column v-for="ben in beneficiaries" :key="ben.id">
      <StewardDelegate class="my-3" :steward="ben"></StewardDelegate>
      <v-divider></v-divider>
    </v-layout>
    <DefaultText v-if="beneficiaries.length == 0">No stewards</DefaultText>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      beneficiaries: [],
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    StewardDelegate: () =>
      import("@/components/delegates/projects/StewardDelegate"),
  },
  async fetch() {
    this.beneficiaries = await this.$axios
      .get(`projects/${this.project.id}/assignments/`)
      .then((reply) => reply.data);
  },
};
</script>