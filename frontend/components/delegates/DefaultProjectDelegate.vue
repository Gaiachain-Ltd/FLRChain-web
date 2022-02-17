<template>
  <v-card @click.prevent="details" ma-0>
    <v-layout column ma-0 pa-6>
      <v-layout align-center>
        <DefaultText :size="18" :color="$vuetify.theme.themes.light.primary">{{
          project.title
        }}</DefaultText>
        <v-spacer></v-spacer>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.quinary"
          >Active</DefaultText
        >
        <StatusIndicator class="ml-1" :color="indicatorColor"></StatusIndicator>
      </v-layout>
      <v-layout align-center>
        <DefaultSVGIcon
          class="mb-1 mr-2"
          :icon="require('@/assets/icons/date.svg')"
          size="12"
        ></DefaultSVGIcon>
        <DefaultText :size="12">{{ timePeriod }}</DefaultText>
      </v-layout>
      <v-layout>
        <v-img
          :src="require('@/assets/images/placeholder.png')"
          class="mt-6"
          contain
        ></v-img>
      </v-layout>
      <v-layout class="my-6">
        <DefaultText :size="14">{{ project.description }}</DefaultText>
      </v-layout>
      <v-layout>
        <v-spacer></v-spacer>
        <ActionButton
          label="My contribution"
          color="white"
          :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
          :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        ></ActionButton>
        <ActionButton
          class="ml-3"
          label="Details"
          color="primary"
        ></ActionButton>
      </v-layout>
    </v-layout>
  </v-card>
</template>

<script>
import { mapActions } from "vuex";
import moment from "moment";
import { STATUS } from "@/constants/project";

export default {
  props: {
    project: {},
  },
  components: {
    StatusIndicator: () =>
      import("@/components/widgets/projects/StatusIndicator"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    LabeledTextWithIcon: () => import("@/components/texts/LabeledTextWithIcon"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  computed: {
    indicatorColor() {
      switch (this.project.status) {
        case STATUS.FUNDRAISING:
          return this.$vuetify.theme.themes.light.primary;
        case STATUS.ACTIVE:
          return this.$vuetify.theme.themes.light.success;
        case STATUS.CLOSED:
          return this.$vuetify.theme.themes.light.error;
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
    timePeriod() {
      const start = moment(this.project.start).format("MMMM DD, YYYY");
      const end = moment(this.project.end).format("MMMM DD, YYYY");
      return `${start} - ${end}`;
    },
  },
  methods: {
    ...mapActions(["updateDetailsProjectId"]),
    details() {
      this.updateDetailsProjectId(this.project.id);
      this.$router.push(
        `/project/${this.$route.params.status || "all"}/details`
      );
    },
    formattedValue(value) {
      return `${parseFloat(value)} USDC`;
    },
  },
};
</script>