<template>
  <v-btn
    v-bind="$attrs"
    v-on="$listeners"
    :class="[
      'text-none elevation-0 my-1 mr-1 default',
      creator && 'creator',
      highlight && 'highlight',
    ]"
  >
    <v-layout align-center>
      <DefaultSVGIcon
        v-if="showPrepIcon"
        :icon="highlight ? icons[tagType].highlightIcon : icons[tagType].icon"
        size="15"
        class="mb-1 mr-2"
      ></DefaultSVGIcon>
      <span class="text-truncate">
        <slot></slot>
      </span>
      <DefaultSVGIcon
        v-if="showDeleteIcon"
        :icon="require('@/assets/icons/delete.svg')"
        size="15"
        class="mb-1 ml-2"
      ></DefaultSVGIcon>
    </v-layout>
  </v-btn>
</template>

<script>
export default {
  props: {
    creator: {
      type: Boolean,
      default: false,
    },
    highlight: {
      type: Boolean,
      default: false,
    },
    showDeleteIcon: {
      type: Boolean,
      default: false,
    },
    showPrepIcon: {
      type: Boolean,
      default: false,
    },
    tagType: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      icons: {
        0: {
          //TEXT
          icon: require("@/assets/icons/edit.svg"),
          highlightIcon: require("@/assets/icons/edit-white.svg"),
        },
        1: {
          //NUMBER
          icon: require("@/assets/icons/hashtag.svg"),
          highlightIcon: require("@/assets/icons/hashtag-white.svg"),
        },
        2: {
          //AREA
          icon: require("@/assets/icons/area.svg"),
          highlightIcon: require("@/assets/icons/area-white.svg"),
        },
        3: {
          //PHOTO
          icon: require("@/assets/icons/upload.svg"),
          highlightIcon: require("@/assets/icons/upload-white.svg"),
        },
      },
    };
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>

<style scoped>
.default {
  color: var(--v-quaternary-base);
  border-style: solid;
  border-color: var(--v-quaternary-base);
  border-radius: 20px;
  border-width: 1px;
  padding-top: 3px !important;
  background-color: white !important;
  max-width: 100%;
}
.default ::v-deep .v-btn__content {
  width: 100%;
  white-space: normal;
}
.creator {
  background-color: #f7f9fb !important;
}
.highlight {
  color: white !important;
  background-color: var(--v-primary-base) !important;
  border-color: var(--v-primary-base) !important;
}
button.v-btn[disabled] {
  opacity: 0.3;
}
</style>