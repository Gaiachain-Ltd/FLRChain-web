<template>
  <div>
    <v-card :width="width" class="auth-transition elevation-16" >
      <v-card-title class="px-6">
        <div class="auth-title">{{ title }}</div>
      </v-card-title>
      <v-card-subtitle class="px-6">
        <DefaultText class="mt-1">{{ subtitle }}</DefaultText>
      </v-card-subtitle>
      <v-card-text class="px-6">
        <v-divider></v-divider>
        <slot name="content"></slot>
        <v-divider></v-divider>
      </v-card-text>
      <v-card-actions class="px-6">
        <v-layout column align-center>
          <slot name="footer"></slot>
        </v-layout>
      </v-card-actions>
    </v-card>
    <ErrorPopup
      v-if="errorPopupVisible"
      :value.sync="errorPopupVisible"
    ></ErrorPopup>
    <SuccessPopup
      v-if="successPopupVisible"
      :value.sync="successPopupVisible"
      :text="successPopupText"
    ></SuccessPopup>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    },
    subtitle: {
      type: String,
    },
  },
  computed: {
    width() {
      switch (this.$vuetify.breakpoint.name) {
        case "xs":
          return 350;
        case "sm":
          return 400;
        case "md":
          return 450;
        case "lg":
          return 500;
        case "xl":
          return 550;
      }
    },
  },
  data() {
    return {
      errorPopupVisible: false,
      successPopupVisible: false,
      successPopupText: "",
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ErrorPopup: () => import("@/components/popups/ErrorPopup"),
    SuccessPopup: () => import("@/components/popups/SuccessPopup"),
  },
  methods: {
    showErrorPopup() {
      this.errorPopupVisible = true;
    },
    showSuccessPopup(text) {
      this.successPopupText = text;
      this.successPopupVisible = true;
    },
  },
};
</script>

<style scoped>
.auth-title {
  font-family: "open-sans" !important;
  font-weight: 400 !important;
  font-size: 28px !important;
  line-height: 40px !important;
  color: var(--v-quinary-base);
}
.auth-transition {
  -moz-transition: width 1s ease-in-out, left 1.5s ease-in-out;
  -webkit-transition: width 1s ease-in-out, left 1.5s ease-in-out;
  -o-transition: width 1s ease-in-out, left 1.5s ease-in-out;
  transition: width 1s ease-in-out, left 1.5s ease-in-out;
}
</style>
