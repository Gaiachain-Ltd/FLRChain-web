<template>
  <v-layout column>
    <template v-for="tag in data.tags">
      <v-layout
        :key="tag.id"
        column
        class="ma-1"
        v-if="tag.tag_type != PHOTO_TYPE"
      >
        <DefaultText :size="14" bold>{{ tag.name }}</DefaultText>
        {{ tagValue(tag) }}
      </v-layout>
    </template>
  </v-layout>
</template>

<script>
import { TAG_TYPES } from "@/constants/project";

export default {
  props: {
    data: {},
  },
  data() {
    return {
      PHOTO_TYPE: TAG_TYPES.PHOTO_TYPE,
    };
  },
  methods: {
    tagValue(tag) {
      switch (tag.tag_type) {
        case TAG_TYPES.TEXT_TYPE:
          return this.data.text || "-";
        case TAG_TYPES.NUMBER_TYPE:
          return `${this.data.number} ${tag.unit}` || "-";
        case TAG_TYPES.AREA_TYPE:
          return this.data.area || "-";
        default:
          return;
      }
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>