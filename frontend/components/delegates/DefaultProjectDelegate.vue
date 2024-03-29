<template>
  <v-card @click.prevent="details" ma-0>
    <v-layout column ma-0 pa-6>
      <v-layout align-center>
        <DefaultText :size="18" :color="$vuetify.theme.themes.light.primary">{{
          project.title
        }}</DefaultText>
        <v-spacer></v-spacer>
        <DefaultText :size="12" class="mb-1" :color="$vuetify.theme.themes.light.quinary">{{
          indicatorTitle
        }}</DefaultText>
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
        <v-img :src="source" class="mt-6" max-height="300"></v-img>
      </v-layout>
      <v-layout
        v-if="project.state == 3 && isFacililator"
        align-center
        class="fundraising-fail pt-2 pb-1 px-2 my-2"
      >
        <DefaultText :size="14" color="white">
          Fundraising period is finished. Your goal hasn't been reached!
        </DefaultText>
        <v-spacer></v-spacer>
        <DefaultSVGIcon
          class="mb-1 mx-2"
          :icon="require('@/assets/icons/exclamation-mark.svg')"
          size="14"
        ></DefaultSVGIcon>
      </v-layout>
      <v-layout column class="my-6">
        <MapButton v-if="project.maplink" :link="project.maplink" class="mb-3"></MapButton>
        <DefaultText :size="14">{{ project.description }}</DefaultText>
      </v-layout>
      <v-layout>
        <v-spacer></v-spacer>
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
import { mapGetters, mapActions } from "vuex";
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
    ActionButton: () => import("@/components/buttons/ActionButton"),
    MapButton: () => import("@/components/buttons/MapButton"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    indicatorColor() {
      switch (this.project.status) {
        case STATUS.FUNDRAISING:
          return "#ff9123";
        case STATUS.ACTIVE:
          return "#00B854";
        case STATUS.CLOSED:
          return "#0075DC";
      }
    },
    indicatorTitle() {
      switch (this.project.status) {
        case STATUS.FUNDRAISING:
          return "Fundraising";
        case STATUS.ACTIVE:
          return "Active";
        case STATUS.CLOSED:
          return "Closed";
      }
    },
    timePeriod() {
      const start = moment(this.project.start).format("MMMM DD, YYYY");
      const end = moment(this.project.end).format("MMMM DD, YYYY");
      return `${start} - ${end}`;
    },
    source() {
      if (this.project.image) {
        return `${this.$config.baseUrl}/${this.project.image}`;
      } else {
        return require("@/assets/images/placeholder.png");
      }
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

<style scoped>
.fundraising-fail {
  background-color: #ff9123;
  border-radius: 5px;
}
</style>