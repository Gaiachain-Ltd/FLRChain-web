<template>
  <DefaultProjectDetails :project="project">
    <v-layout column ma-0>
      <v-layout row ma-0 mt-6>
        <v-flex xs6>
          <LabeledTextWithIcon
            label="Project deadline"
            :text="project.end"
            :icon="dateIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
        <v-flex xs6>
          <LabeledTextWithIcon
            class="xs6"
            label="Investment time"
            :text="investmentTime"
            :icon="dateIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
      </v-layout>
      <v-layout row ma-0 mt-6>
        <v-flex xs6>
          <LabeledTextWithIcon
            class="xs6"
            label="Invested USDC"
            :text="investedAmount"
            :icon="usdcIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
        <v-flex xs6>
          <LabeledTextWithIcon
            class="xs6"
            :label="investStatus"
            :text="spentAmount"
            :icon="usdcIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
      </v-layout>
    </v-layout>
  </DefaultProjectDetails>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    project: {},
  },
  data() {
    return {
      activeIcon: require("@/assets/icons/active.svg"),
      inactiveIcon: require("@/assets/icons/inactive.svg"),
      usdcIcon: require("@/assets/icons/usdc.svg"),
      dateIcon: require("@/assets/icons/date.svg"),
    };
  },
  components: {
    ...mapGetters(["isFacililator"]),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    LabeledTextWithIcon: () => import("@/components/texts/LabeledTextWithIcon"),
    DefaultProjectDetails: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
  },
  computed: {
    investmentTime() {
      return `${this.project.investment.start} - ${this.project.investment.end}`;
    },
    investedAmount() {
      return this.formattedValue(this.project.investment.amount);
    },
    spentAmount() {
      return this.formattedValue(this.project.investment.amount);
    },
    icon() {
      return this.project.investment.status
        ? this.activeIcon
        : this.inactiveIcon;
    },
    investStatus() {
      return this.isFacililator ? "Gain USDC" : "Spent USDC";
    },
  },
  methods: {
    details() {
      this.$router.push(`/project/${this.project.id}`);
    },
    formattedValue(value) {
      return `${parseFloat(value)} USDC`;
    },
  },
};
</script>