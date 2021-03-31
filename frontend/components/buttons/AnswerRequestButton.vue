<template>
  <DefaultPopup :show.sync="showPopup">
    <template v-slot="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        class="answer-btn-style elevation-0 round text-none white--text"
        height="20"
        color="septenary"
        >Answer request</v-btn
      >
    </template>
    <v-flex slot="content" my-6>
      <DefaultText
        class="text-center"
        :size="22"
        color="#253F50"
        family="open-sans"
        ><b>{{ name }}</b> ask you for permission to join project</DefaultText
      >
    </v-flex>
    <v-layout slot="buttons" column ma-0 style="width: 100%">
      <v-flex mb-3>
        <BlockButton @clicked="accept">Accept</BlockButton>
      </v-flex>
      <v-flex>
        <BlockButton color="error" @clicked="reject">Reject</BlockButton>
      </v-flex>
    </v-layout>
  </DefaultPopup>
</template>

<script>
export default {
  props: {
    assignment: {},
  },
  data() {
    return {
      showPopup: false,
    };
  },
  computed: {
    name() {
      return `${this.assignment.beneficiary.first_name} ${this.assignment.beneficiary.last_name}`;
    },
  },
  components: {
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    BlockButton: () => import("@/components/buttons/BlockButton"),
  },
  methods: {
    async accept() {
      await this.$axios
        .put(`projects/assignments/${this.assignment.id}/`, {
          status: 1,
        })
        .then(() => this.$emit("refresh"));
      this.showPopup = false;
    },
    async reject() {
      await this.$axios
        .put(`projects/assignments/${this.assignment.id}/`, {
          status: 0,
        })
        .then(() => this.$emit("refresh"));
      this.showPopup = false;
    },
  },
};
</script>

<style scoped>
.answer-btn-style {
  border-radius: 7px !important;
  font-family: "open-sans" !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  letter-spacing: -0.24px !important;
}
</style>