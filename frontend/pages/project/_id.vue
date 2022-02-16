<template>
  <v-layout column pa-6>
    <ToolBar title="Project details"> </ToolBar>
    <FundraisingProgressCard
      class="mb-6"
      :project="project"
    ></FundraisingProgressCard>
    <v-layout shrink :class="$vuetify.breakpoint.xsOnly && 'wrap'">
      <v-flex xs12 md9 shrink>
        <v-layout column>
          <DetailsProjectCard
            v-if="!edit"
            class="mb-6"
            :project="project"
          ></DetailsProjectCard>
          <InputProjectCard
            v-else
            class="mb-6"
            :project.sync="project"
          ></InputProjectCard>
          <DetailsMilestonesCard
            v-if="!edit"
            class="mb-6"
            :project="project"
          ></DetailsMilestonesCard>
          <InputTasksCard
            v-else
            class="mb-6"
            :project.sync="project"
          ></InputTasksCard>
          <DetailsBlockchainCard :project="project"></DetailsBlockchainCard>
          <v-spacer></v-spacer>
        </v-layout>
      </v-flex>
      <v-flex xs12 md5 shrink>
        <v-layout column :class="!$vuetify.breakpoint.xsOnly && 'ml-6'">
          <client-only v-if="project.investment" placeholder="Loading...">
            <DetailsInvestmentCard class="mb-6"></DetailsInvestmentCard>
          </client-only>
          <client-only v-if="isFacililator" placeholder="Loading...">
            <BeneficiariesCard class="mb-6"></BeneficiariesCard>
          </client-only>
          <client-only
            v-if="!isFacililator && project.status == 0"
            placeholder="Loading..."
          >
            <InputInvestmentCard
              v-if="project.start"
              @refresh="$fetch"
              :project="project"
              :disabled="!$auth.user.opted_in"
            ></InputInvestmentCard>
          </client-only>
          <client-only placeholder="Loading...">
            <DetailsInvestorsCard class="mb-6"></DetailsInvestorsCard>
          </client-only>
        </v-layout>
      </v-flex>
    </v-layout>
    <WorkHistoryCard v-if="project.investment"></WorkHistoryCard>
    <v-spacer></v-spacer>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
    <SuccessPopup
      v-if="successPopupVisible"
      :value.sync="successPopupVisible"
      text="Project has been saved successfully."
    ></SuccessPopup>
    <InfoPopup
      v-if="infoPopupVisible"
      :value.sync="infoPopupVisible"
      :text="info"
    ></InfoPopup>
  </v-layout>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      info: "",
      infoPopupVisible: false,
      errorPopupVisible: false,
      successPopupVisible: false,
      project: {},
      edit: false,
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    DetailsProjectCard: () =>
      import("@/components/cards/project/DetailsProjectCard"),
    DetailsMilestonesCard: () =>
      import("@/components/cards/project/DetailsMilestonesCard"),
    BeneficiariesCard: () =>
      import("@/components/cards/project/BeneficiariesCard"),
    InputInvestmentCard: () =>
      import("@/components/cards/project/InputInvestmentCard"),
    DetailsInvestmentCard: () =>
      import("@/components/cards/project/DetailsInvestmentCard"),
    WorkHistoryCard: () => import("@/components/cards/project/WorkHistoryCard"),
    DetailsInvestorsCard: () =>
      import("@/components/cards/project/DetailsInvestorsCard"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    InputTasksCard: () => import("@/components/cards/project/InputTasksCard"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
    ProjectStatusLabel: () => import("@/components/texts/ProjectStatusLabel"),
    InfoPopup: () => import("@/components/popups/InfoPopup"),
    DetailsBlockchainCard: () =>
      import("@/components/cards/project/DetailsBlockchainCard"),
    FundraisingProgressCard: () =>
      import("@/components/cards/project/FundraisingProgressCard"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    isFinished() {
      return this.project.investment && this.project.investment.status === 0;
    },
    projectStatus() {
      if (this.project.investment) {
        if (this.isFinished) {
          return "Finished";
        } else {
          return "Ongoing";
        }
      } else {
        return "Waiting for investor";
      }
    },
  },
  methods: {
    handleEdit() {
      if (this.edit) {
        this.$axios
          .put(`projects/${this.$route.params.id}/`, this.project)
          .then((reply) => {
            this.project = reply.data;
            this.successPopupVisible = true;
          })
          .catch(() => (this.errorPopupVisible = true));
      }
      this.edit = !this.edit;
    },
  },
  async fetch() {
    this.project = await this.$axios
      .get(`projects/${this.$route.params.id}/`)
      .then((reply) => reply.data)
      .catch(() => (this.errorPopupVisible = true));

    if (!this.$auth.user.opted_in) {
      this.$auth.fetchUser().then(() => {
        if (!this.$auth.user.opted_in) {
          this.info = "Your account is not active yet. Please try again later.";
          this.infoPopupVisible = true;
        }
      });
    } else if (this.project.investment && !this.project.investment.confirmed) {
      this.info = "Investment has not been confirmed yet.";
      this.infoPopupVisible = true;
    }
  },
};
</script>
