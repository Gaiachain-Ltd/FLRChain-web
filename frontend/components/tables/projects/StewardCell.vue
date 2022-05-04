<template>
  <v-layout @click.prevent="showProfile">
    <a href="">{{ profile.name }}</a>
    <ProfilePopup
      v-if="show"
      v-model="show"
      :profileId="profile.id"
    ></ProfilePopup>
  </v-layout>
</template>

<script>
export default {
  props: {
    profile: {},
  },
  data() {
    return {
      show: false,
    };
  },
  components: {
    ProfilePopup: () => import("@/components/popups/profile/ProfilePopup"),
  },
  methods: {
    showProfile() {
      this.show = true;
    },
  },
};
</script>