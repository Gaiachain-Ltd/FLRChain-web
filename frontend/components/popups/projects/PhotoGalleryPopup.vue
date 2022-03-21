<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"></v-flex>
    <v-flex slot="content" ma-6>
      <v-layout column v-if="images.length > 0">
        <v-img :src="source" contain></v-img>
        <v-layout class="mt-3">
          <ActionButton
            :disabled="!moreThanOnePhoto"
            color="primary"
            @click.prevent="onPrev"
            >Prev</ActionButton
          >
          <v-spacer></v-spacer>
          <ActionButton
            class="mr-3"
            color="white"
            :border="`1px ${$vuetify.theme.themes.light.primary} solid !important`"
            :textColor="`${$vuetify.theme.themes.light.primary} !important`"
            @click.prevent="show = false"
            >Close</ActionButton
          >
          <v-spacer></v-spacer>
          <ActionButton
            :disabled="!moreThanOnePhoto"
            color="primary"
            @click.prevent="onNext"
            >Next</ActionButton
          >
        </v-layout>
      </v-layout>
    </v-flex>
  </DefaultPopup>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
    },
    activity: {},
  },
  data() {
    return {
      index: 0,
      images: [],
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
    source() {
      return `${this.$config.baseUrl}/${this.images[this.index].file}`;
    },
    moreThanOnePhoto() {
      return this.images.length > 1;
    },
  },
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
  },
  methods: {
    onNext() {
      if (this.index + 1 > this.images.length - 1) {
        this.index = 0;
      } else {
        this.index += 1;
      }
    },
    onPrev() {
      if (this.index - 1 < 0) {
        this.index = 0;
      } else {
        this.index -= 1;
      }
    },
  },
  async fetch() {
    this.images = await this.$axios
      .get(`projects/activity/${this.activity.id}/photo/`)
      .then((reply) => reply.data);
    console.log("IMAGES", this.images);
  },
};
</script>