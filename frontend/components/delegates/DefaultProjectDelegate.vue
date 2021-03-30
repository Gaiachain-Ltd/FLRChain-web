<template>
  <v-hover v-slot="{ hover }">
    <v-card @click.prevent="details" ma-0>
      <v-layout column ma-0 pa-6>
        <v-layout row ma-0 align-center>
          <DefaultSVGIcon
            v-if="icon !== ''"
            class="mb-1 mr-3"
            :icon="icon"
          ></DefaultSVGIcon>
          <DefaultText
            :size="18"
            :color="hover ? hoverColor : $vuetify.theme.themes.light.quinary"
            >{{ project.title }}</DefaultText
          >
          <v-spacer></v-spacer>
          <DefaultSVGIcon
            v-if="hover"
            class="mb-1 mr-3"
            :icon="arrowIcon"
          ></DefaultSVGIcon>
        </v-layout>
        <slot></slot>
      </v-layout>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    LabeledTextWithIcon: () => import("@/components/texts/LabeledTextWithIcon"),
  },
  computed: {
    hoverColor() {
      if (!this.project.investment) {
        return this.$vuetify.theme.themes.light.secondary;
      } else if (this.project.investment.status === 0) {
        return this.$vuetify.theme.themes.light.error;
      } else {
        return this.$vuetify.theme.themes.light.primary;
      }
    },
    icon() {
      if (!this.project.investment) {
        return "";
      } else if (this.project.investment.status === 0) {
        return require("@/assets/icons/inactive.svg");
      } else {
        return require("@/assets/icons/active.svg");
      }
    },
    arrowIcon() {
      if (!this.project.investment) {
        return require("@/assets/icons/arrow-project-blue.svg");
      } else if (this.project.investment.status === 0) {
        return require("@/assets/icons/arrow-project-red.svg");
      } else {
        return require("@/assets/icons/arrow-project-green.svg");
      }
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