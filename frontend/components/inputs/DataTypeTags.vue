<template>
  <v-layout column class="mb-4">
    <DefaultText
      class="mb-2"
      :size="12"
      :color="$vuetify.theme.themes.light.senary"
      >Type of data*</DefaultText
    >
    <v-layout wrap>
      <TagButton
        v-if="task.data_type_tag"
        :showDeleteIcon="!readonly"
        :class="readonly && 'no-events'"
        @click.prevent="showConfirmPopup = true"
        >{{ task.data_type_tag.name }}</TagButton
      >
      <TagButton
        v-if="!readonly"
        creator
        @click.prevent="showAddPopup = true"
        :disabled="!!task.data_type_tag"
        >+ Add type</TagButton
      >
    </v-layout>
    <v-flex v-if="error && !task.data_type_tag">
      <DefaultText :size="12" class="error--text">
        Tag is required.
      </DefaultText>
    </v-flex>
    <DataTypeTagPopup
      v-if="showAddPopup"
      v-model="showAddPopup"
      :task.sync="task"
    ></DataTypeTagPopup>
    <ConfirmPopup
      v-model="showConfirmPopup"
      text="Do you really want to remove this tag?"
      @confirm="deleteTag"
    ></ConfirmPopup>
  </v-layout>
</template>

<script>
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
      showAddPopup: false,
      showConfirmPopup: false,
      error: false,
    };
  },
  components: {
    TagButton: () => import("@/components/buttons/TagButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    ConfirmPopup: () => import("@/components/popups/ConfirmPopup"),
    DataTypeTagPopup: () =>
      import("@/components/popups/projects/DataTypeTagPopup"),
  },
  methods: {
    deleteTag() {
      this.$set(this.task, "data_type_tag", undefined);
      this.error = true;
    },
    validate() {
      if (!this.task.data_type_tag) {
        this.error = true;
        return false;
      }
      this.error = false;
      return true;
    },
  },
};
</script>

<style scoped>
.no-events {
  pointer-events: none;
}
</style>