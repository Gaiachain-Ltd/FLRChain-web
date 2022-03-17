<template>
  <v-layout column class="mb-4">
    <DefaultText
      class="mb-2"
      :size="12"
      :color="$vuetify.theme.themes.light.senary"
      >Required data</DefaultText
    >
    <v-layout>
      <TagButton
        v-for="tag in task.data_tags"
        :key="tag.id"
        :tagType="tag.tag_type"
        :showDeleteIcon="!readonly"
        :class="readonly && 'no-events'"
        @click.prevent="() => handleConfirm(tag.id)"
        showPrepIcon
        >{{
          tag.tag_type == 1 ? `${tag.name} (${tag.unit})` : tag.name
        }}</TagButton
      >
      <TagButton v-if="!readonly" creator @click.prevent="showAddPopup = true"
        >+ Add tag</TagButton
      >
    </v-layout>
    <DataTagPopup
      v-if="showAddPopup"
      v-model="showAddPopup"
      :task.sync="task"
    ></DataTagPopup>
    <ConfirmPopup
      v-model="showConfirmPopup"
      text="Do you really want to remove this tag?"
      @confirm="deleteTag"
    ></ConfirmPopup>
  </v-layout>
</template>

<script>
import _ from "lodash";

export default {
  props: {
    task: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      tagToDeleteId: 0,
      showAddPopup: false,
      showConfirmPopup: false,
    };
  },
  components: {
    DataTagPopup: () => import("@/components/popups/projects/DataTagPopup"),
    ConfirmPopup: () => import("@/components/popups/ConfirmPopup"),
    TagButton: () => import("@/components/buttons/TagButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
  methods: {
    handleConfirm(id) {
      this.tagToDeleteId = id;
      this.showConfirmPopup = true;
    },
    deleteTag() {
      const index = _.findIndex(this.task.data_tags, {
        id: this.tagToDeleteId,
      });
      if (index != -1) {
        this.task.data_tags.splice(index, 1);
      }
    },
  },
};
</script>

<style scoped>
.no-events {
  pointer-events: none;
}
</style>