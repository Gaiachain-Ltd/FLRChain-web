<template>
  <v-layout column>
    <FundraisingProgressCard
    ref="progress"
      class="ma-3"
      :project="project"
    ></FundraisingProgressCard>
    <v-layout wrap>
      <v-col class="ma-0 pa-3" md="8" sm="12">
        <DetailsBlockchainCard :project="project"></DetailsBlockchainCard>
      </v-col>
      <v-col class="ma-0 pa-3" md="4" sm="12" v-if="!isFacililator">
        <InputInvestmentCard :project="project" @refresh="onRefresh"></InputInvestmentCard>
      </v-col>
      <v-col
        :class="['ma-0 pa-3', !isFacililator && isFundraising && 'order-md-2']"
        md="4"
        sm="12"
      >
        <DetailsStewardsCard :project="project"></DetailsStewardsCard>
      </v-col>
      <v-col class="ma-0 pa-3" :md="!isFundraising ? 12 : 8" sm="12">
        <InputProjectCard
          :project.sync="project"
          :readonly="!isFacililator || isSyncing"
        ></InputProjectCard>
      </v-col>
    </v-layout>
    <ActionBarCard
      class="ma-3"
      v-if="isFacililator"
      @save="update"
      hideCancel
      :loading="isSyncing"
    ></ActionBarCard>
  </v-layout>
</template>

<script>
import ProjectMixin from "@/mixins/ProjectMixin";
import { SYNC, STATUS } from "@/constants/project";
import { mapGetters } from "vuex";

export default {
  mixins: [ProjectMixin],
  data() {
    return {
      FUNDRAISING: STATUS.FUNDRAISING,
    };
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    isFundraising() {
      return this.project.status == this.FUNDRAISING;
    },
  },
  components: {
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
    DetailsBlockchainCard: () =>
      import("@/components/cards/project/DetailsBlockchainCard"),
    DetailsStewardsCard: () =>
      import("@/components/cards/project/DetailsStewardsCard"),
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
  },
  methods: {
    update() {
      this.project.sync = SYNC.TO_SYNC;
      this.$axios
        .put(`projects/${this.project.id}/`, this.project)
        .then((reply) => {
          this.requestRefresh();
          this.onProjectUpdate(reply.data);
        });
    },
    fetch() {
      this.$axios.get(`projects/${this.project.id}/`).then((reply) => {
        if (!this.requestRefresh()) {
          this.onProjectUpdate(reply.data);
        }
      });
    },
    onProjectUpdate(project) {
      this.$emit("update:project", project);
    },
    onRefresh() {
      this.$refs.progress.$fetch();
    }
  },
  mounted() {
    this.requestRefresh();
  },
};
</script>