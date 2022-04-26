<template>
  <DefaultPopup :show.sync="show" maxWidth="500">
    <v-flex slot="icon"></v-flex>
    <v-flex slot="content" ma-6>
      <v-layout column>
        <DefaultText>Profile details</DefaultText>
        <StewardProfileForm class="mt-3" v-model="profile" readonly></StewardProfileForm>
      </v-layout>
    </v-flex>
    <v-layout slot="buttons" mb-6 mx-6>
      <v-spacer></v-spacer>
      <ActionButton
        class="mr-3"
        color="white"
        :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
        :textColor="`${$vuetify.theme.themes.light.primary} !important`"
        @click.prevent="show = false"
        >Close</ActionButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
    },
    profileId: {
      type: Number | String,
    },
  },
  data() {
    return {
      profile: {},
    };
  },
  computed: {
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    StewardProfileForm: () =>
      import("@/components/forms/profile/StewardProfileForm"),
  },
  async fetch() {
    this.$axios
      .get(`info/${this.profileId}/`)
      .then((reply) => {
        this.profile = reply.data;
      })
      .catch((error) => {
        console.log("ERROR", error);
      });
  },
};
</script>