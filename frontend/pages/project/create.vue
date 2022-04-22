<template>
  <v-layout column fill-height pa-6>
    <ToolBar title="Create project"></ToolBar>
    <InputProjectCard
      ref="inputProject"
      class="pb-0"
      :project.sync="project"
    ></InputProjectCard>
    <ActionBarCard
      class="mt-6"
      saveBtnText="Create project"
      :disabled="!$auth.user.opted_in"
      @save="handleCreate"
      @cancel="handleCancel"
    ></ActionBarCard>
    <v-spacer></v-spacer>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
      :text="errorText"
    ></ErrorPopup>
    <InfoPopup
      v-if="infoPopupVisible"
      :value.sync="infoPopupVisible"
      text="Your account is not active yet. Please try again later."
    ></InfoPopup>
  </v-layout>
</template>

<script>
import { mapActions } from "vuex";
import { STATUS } from "@/constants/project";

export default {
  data() {
    return {
      infoPopupVisible: false,
      errorPopupVisible: false,
      errorText: "",
      project: {
        title: "",
        description: "",
        start: this.$moment().format("YYYY-MM-DD"),
        end: this.$moment().format("YYYY-MM-DD"),
        fac_adm_funds: "0",
        status: STATUS.FUNDRAISING,
        actions: [
          {
            name: "",
            milestones: [
              {
                name: "",
                tasks: [
                  {
                    name: "",
                    instructions: "",
                    batch: "0",
                    reward: "0",
                    count: 1,
                  },
                ],
              },
            ],
          },
        ],
      },
    };
  },
  components: {
    ToolBar: () => import("@/components/toolbar/ToolBar"),
    InputProjectCard: () =>
      import("@/components/cards/project/InputProjectCard"),
    ActionBarCard: () => import("@/components/cards/ActionBarCard"),
    DefaultTitle: () => import("@/components/texts/DefaultTitle"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    InfoPopup: () => import("@/components/popups/InfoPopup"),
    ProjectForm: () => import("@/components/forms/project/ProjectForm"),
  },
  computed: {
    blocked() {
      return this.$auth.user.opted_in;
    },
  },
  methods: {
    ...mapActions(["updateDetailsProjectId"]),
    handleCreate() {
      if (this.$refs.inputProject.validate()) {
        this.$axios
          .post("projects/", this.project)
          .then((reply) => {
            if (this.project.fileToUpload) {
              let formData = new FormData();
              formData.append("image", this.project.fileToUpload);
              this.$axios
                .put(`projects/${reply.data.id}/image/`, formData)
                .then(() => {
                  this.updateDetailsProjectId(reply.data.id);
                  this.$router.replace("/project/all/details");
                })
                .catch(() => this.showErrorPopup());
            } else {
                this.updateDetailsProjectId(reply.data.id);
                this.$router.replace("/project/all/details");
            }
          })
          .catch(() => this.showErrorPopup());
      } else {
        this.showErrorPopup("Please correct fields marked on red.");
      }
    },
    handleCancel() {
      this.$router.back();
    },
    showErrorPopup(text) {
      if (text) {
        this.errorText = text;
      } else {
        this.errorText = "Something went wrong. Please try again later.";
      }
      this.errorPopupVisible = true;
    },
  },
  async fetch() {
    if (!this.$auth.user.opted_in) {
      this.$auth.fetchUser().then(() => {
        if (!this.$auth.user.opted_in) {
          this.infoPopupVisible = true;
        }
      });
    }
  },
};
</script>

<style scoped>
.placeholder {
  width: 100% !important;
  height: 82px !important;
}
</style>