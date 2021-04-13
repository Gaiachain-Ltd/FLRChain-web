<template>
  <v-card mb-0>
    <v-layout column ma-0 pa-6>
      <v-flex mb-6>
        <LabeledText
          label="Project status"
          :text="projectStatus"
          :icon="projectStatusIcon"
        ></LabeledText>
      </v-flex>
      <v-flex mb-6>
        <LabeledText
          label="Project time"
          :text="projectTime"
          :icon="dateIcon"
        ></LabeledText>
      </v-flex>
      <v-flex mb-6 v-if="project.investment">
        <LabeledText
          label="Investment time"
          :text="investmentTime"
          :icon="dateIcon"
        ></LabeledText>
      </v-flex>
      <v-flex mb-6>
        <LabeledText
          label="Facilitator"
          :text="project.facililator"
        ></LabeledText>
      </v-flex>
      <v-flex>
        <LabeledText
          label="Description"
          :text="project.description"
        ></LabeledText>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      ongoingIcon: require("@/assets/icons/icon-status-ongoing.svg"),
      waitingIcon: require("@/assets/icons/icon-status-waiting.svg"),
      finishedIcon: require("@/assets/icons/icon-status-finished.svg"),
      dateIcon: require("@/assets/icons/date.svg"),
    };
  },
  computed: {
    isFinished() {
      return this.project.investment && this.project.investment.status === 0;
    },
    projectTime() {
      return `${this.project.start} - ${this.project.end}`;
    },
    investmentTime() {
      return `${this.project.investment.start} - ${this.project.investment.end}`;
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
    projectStatusIcon() {
      if (this.project.investment) {
        if (this.isFinished) {
          return this.finishedIcon;
        } else {
          return this.ongoingIcon;
        }
      } else {
        return this.waitingIcon;
      }
    },
  },
  components: {
    LabeledText: () => import("@/components/texts/LabeledText"),
  },
};
</script>