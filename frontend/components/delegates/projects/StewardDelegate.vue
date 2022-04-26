<template>
  <v-layout @click.prevent="showPopup">
    <a href="">{{ steward.name }}</a>
    <v-spacer></v-spacer>
    <DefaultText :color="statusColor(steward.status)" bold>{{
      status(steward.status)
    }}</DefaultText>
    <ProfilePopup
      v-if="show"
      v-model="show"
      :profileId="steward.user_id"
    ></ProfilePopup>
  </v-layout>
</template>

<script>
export default {
  props: {
    steward: {},
  },
  data() {
    return {
      show: false,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ProfilePopup: () => import("@/components/popups/profile/ProfilePopup"),
  },
  methods: {
    status(value) {
      switch (value) {
        case 0:
          return "Pending";
        case 1:
          return "Accepted";
        case 2:
          return "Rejected";
        default:
          return value;
      }
    },
    statusColor(value) {
      switch (value) {
        case 1:
          return this.$vuetify.theme.themes.light.success;
        case 2:
          return this.$vuetify.theme.themes.light.error;
        default:
          return undefined;
      }
    },
    showPopup() {
      this.show = true;
    },
  },
};
</script>