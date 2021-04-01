<template>
  <DefaultPopup :show.sync="showLogoutPopup">
    <template v-slot="{ on, attrs }">
      <v-layout
        class="pointer-cursor"
        row
        shrink
        ma-0
        pa-0
        align-center
        v-on="on"
      >
        <v-layout column ma-0>
          <DefaulText :color="$vuetify.theme.themes.light.quinary">{{
            `${$auth.user.first_name} ${$auth.user.last_name}`
          }}</DefaulText>
          <div class="account-type-text">{{ accountType }}</div>
        </v-layout>
        <v-flex class="logout-icon-style" shrink ml-4>
          <DefaultSVGIcon
            :icon="require('@/assets/toolbar/logout.svg')"
          ></DefaultSVGIcon>
        </v-flex>
      </v-layout>
    </template>
    <v-flex slot="icon">
      <DefaultSVGIcon
        :icon="require('@/assets/popup/logout.svg')"
        :size="70"
      ></DefaultSVGIcon>
    </v-flex>
    <v-flex slot="content" my-6>
      <DefaultText
        class="text-center"
        :size="22"
        color="#253F50"
        family="open-sans"
        >Are you sure you want to log out?</DefaultText
      >
    </v-flex>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton color="error" @clicked="logOut">Log out</BlockButton>
      </v-flex>
      <v-flex>
        <BlockButton class="cancel-style" color="white"  @clicked="cancel">Cancel</BlockButton>
      </v-flex>
    </v-layout>
  </DefaultPopup>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      showLogoutPopup: false,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  computed: {
    ...mapGetters(["isFacililator"]),
    accountType() {
      return this.isFacililator ? "FACILILATOR" : "INVESTOR";
    },
  },
  methods: {
    logOut() {
      this.showLogoutPopup = false;
      this.$auth.logout().then(this.$router.push("/login"));
    },
    cancel() {
      this.showLogoutPopup = false;
    }
  },
};
</script>

<style scoped>
.account-type-text {
  font-size: 10px !important;
  color: var(--v-quinary-base);
}
.logout-icon-style {
  min-width: 20px !important;
  height: 20px !important;
  width: 20px !important;
  min-height: 20px !important;
}
.pointer-cursor {
  cursor: pointer;
}
.cancel-style {
  border: 1px black solid !important;
}
</style>