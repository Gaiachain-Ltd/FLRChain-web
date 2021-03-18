<template>
  <v-layout column mt-2>
    <ToolBar title="Project details"></ToolBar>
    <DefaultTitle class="mt-10 mb-5">{{ project.title }}</DefaultTitle>
    <v-layout row ma-0>
      <v-flex xs8>
        <v-layout column mr-3>
          <DetailsProjectCard
            class="mb-6"
            :project="project"
          ></DetailsProjectCard>
          <DetailsTasksCard :tasks="project.tasks"></DetailsTasksCard>
        </v-layout>
      </v-flex>
      <v-flex xs4>
        <v-layout column ml-3 xs4>
          <client-only v-if="isFacililator" placeholder="Loading...">
            <BeneficiariesCard class="mb-6"></BeneficiariesCard>
          </client-only>
          <client-only
            v-if="!isFacililator && !project.investment"
            placeholder="Loading..."
          >
            <InputInvestmentCard
              class="mb-6"
              @refresh="$fetch"
            ></InputInvestmentCard>
          </client-only>
          <client-only
            v-if="!isFacililator && project.investment"
            placeholder="Loading..."
          >
            <DetailsInvestmentCard class="mb-6"></DetailsInvestmentCard>
          </client-only>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      project: {},
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    DetailsProjectCard: () =>
      import("@/components/cards/project/DetailsProjectCard"),
    DetailsTasksCard: () =>
      import("@/components/cards/project/DetailsTasksCard"),
    BeneficiariesCard: () =>
      import("@/components/cards/project/BeneficiariesCard"),
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
    DetailsInvestmentCard: () =>
      import("@/components/cards/project/DetailsInvestmentCard"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
  },
  async fetch() {
    this.project = await this.$axios
      .get(`projects/${this.$route.params.id}/`)
      .then((reply) => reply.data);
  },
};
</script>