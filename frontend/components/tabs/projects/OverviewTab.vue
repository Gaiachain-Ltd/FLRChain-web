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
        <InputInvestmentCard
          :project="project"
          @refresh="onRefresh"
        ></InputInvestmentCard>
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
          ref="form"
          :project.sync="project"
          :readonly="!isFacililator || project.status === CLOSED || isSyncing"
        ></InputProjectCard>
      </v-col>
    </v-layout>
    <ActionBarCard
      class="ma-3"
      v-if="isFacililator && project.status !== CLOSED"
      @save="update"
      hideCancel
      :loading="isSyncing"
    >
      <ActionButton
        v-if="project.status == FUNDRAISING && project.state == POSTPONED"
        slot="extra"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.error} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.error} !important`"
        @click.prevent="showConfirmPopup"
        >Close project</ActionButton
      >
    </ActionBarCard>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
      :text="errorText"
    ></ErrorPopup>
    <ConfirmPopup
      v-if="confirmClosePopupVisible"
      v-model="confirmClosePopupVisible"
      text="Do you really want to close this project?"
      @confirm="close"
    >
    </ConfirmPopup>
  </v-layout>
</template>

<script>
import ProjectMixin from "@/mixins/ProjectMixin";
import SyncMixin from "@/mixins/SyncMixin";
import { SYNC, STATUS, STATE } from "@/constants/project";
import { mapGetters } from "vuex";

export default {
  mixins: [ProjectMixin, SyncMixin],
  props: {
    isEditing: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      FUNDRAISING: STATUS.FUNDRAISING,
      CLOSED: STATUS.CLOSED,
      POSTPONED: STATE.POSTPONED,
      errorPopupVisible: false,
      errorText: "",
      confirmClosePopupVisible: false,
    };
  },
  watch: {
    projectStringify(old_project, new_project) {
      if (old_project && new_project) {
        let a = JSON.parse(old_project);
        let b = JSON.parse(new_project);
        //Ignore some properties:
        ["state", "status", "sync", "app_id"].forEach((key) => {
          delete a[key];
          delete b[key];
        });
        if (
          !!a.id &&
          !!b.id &&
          a.id == b.id &&
          !!a.actions &&
          !!b.actions &&
          !_.isEqual(a, b)
        ) {
          console.log("EDITED!", a, b);
          this.internalIsEditing = true;
        }
      }
    },
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    internalIsEditing: {
      get() {
        return this.isEditing;
      },
      set(value) {
        this.$emit("update:isEditing", value);
      },
    },
    isFundraising() {
      return this.project.status == this.FUNDRAISING;
    },
    isSyncing() {
      return !this.project || this.project.sync == SYNC.TO_SYNC;
    },
    url() {
      return `projects/${this.project.id}/`;
    },
    projectStringify() {
      if (this.project) {
        return JSON.stringify(this.project);
      } else {
        return "";
      }
    },
  },
  components: {
    ConfirmPopup: () => import("@/components/popups/ConfirmPopup"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
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
    close() {
      this.project.sync = SYNC.TO_SYNC;
      this.$axios.post(`${this.url}close/`, {}).then((reply) => {
        this.requestRefresh();
        this.onUpdate(reply.data);
      });
    },
    update(silent) {
      if (this.$refs.form.validate()) {
        if (!silent) {
          this.project.sync = SYNC.TO_SYNC;
        }
        return this.$axios
          .put(this.url, this.project)
          .then((reply) => {
            this.requestRefresh();
            this.onUpdate(reply.data);
          })
          .catch(() => {
            if (!silent) {
              this.project.sync = SYNC.SYNCED;
            }
            this.showErrorPopup();
          });
      } else {
        this.showErrorPopup("Please correct fields marked on red.");
      }
    },
    onUpdate(project) {
      this.$emit("update:project", project);
      this.$nextTick(() => (this.internalIsEditing = false));
    },
    onRefresh() {
      this.$refs.progress.$fetch();
    },
    showErrorPopup(text) {
      if (text) {
        this.errorText = text;
      } else {
        this.errorText = "Something went wrong. Please try again later.";
      }
      this.errorPopupVisible = true;
    },
    showConfirmPopup() {
      this.confirmClosePopupVisible = true;
    },
  },
  async fetch() {
    this.refresh();
  },
  mounted() {
    this.requestRefresh();
  },
};
</script>

<style scoped>
.snackbar-style ::v-deep .v-snack__wrapper {
  max-width: 100% !important;
  width: 100% !important;
  height: 120px !important;
  border: 0.5px lightgray solid !important;
}
</style>