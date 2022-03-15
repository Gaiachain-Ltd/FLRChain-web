<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"> </v-flex>
    <v-flex slot="content" ma-6>
      <v-layout column>
        <DefaultText :color="$vuetify.theme.themes.light.primary"
          >Add new required data tag</DefaultText
        >
        <v-layout wrap class="mt-3">
          <TagButton
            v-for="tag in tags"
            :key="tag.tagType"
            :highlight="selectedTagType == tag.tagType"
            @click.prevent="selectedTagType = tag.tagType"
            >{{ tag.name }}</TagButton
          >
        </v-layout>
        <v-layout wrap>
          <TextInput
            class="mt-6"
            label="Tag name"
            placeholder="Please enter tag name..."
            v-model="name"
          ></TextInput>
          <TextInput
            v-if="selectedTagType == NUMBER_TYPE"
            label="Unit"
            placeholder="Please enter unit..."
            v-model="unit"
          ></TextInput>
        </v-layout>
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
        >Cancel</ActionButton
      >
      <ActionButton
        color="primary"
        @click.prevent="handleAdd"
        :loading="loading"
        >Add type</ActionButton
      >
    </v-layout>
  </DefaultPopup>
</template>

<script>
import { TAG_TYPES } from "@/constants/project";

export default {
  props: {
    value: {
      type: Boolean,
    },
    task: {},
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
  data() {
    return {
      loading: false,
      name: "",
      unit: "",
      NUMBER_TYPE: TAG_TYPES.NUMBER_TYPE,
      selectedTagType: TAG_TYPES.TEXT_TYPE,
      tags: [
        {
          icon: "",
          name: "Text",
          tagType: TAG_TYPES.TEXT_TYPE,
        },
        {
          icon: "",
          name: "Number",
          tagType: TAG_TYPES.NUMBER_TYPE,
        },
        {
          icon: "",
          name: "Area",
          tagType: TAG_TYPES.AREA_TYPE,
        },
        {
          icon: "",
          name: "Photo",
          tagType: TAG_TYPES.PHOTO_TYPE,
        },
      ],
    };
  },
  components: {
    TagButton: () => import("@/components/buttons/TagButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
  methods: {
    async handleAdd() {
      this.loading = true;
      await this.$axios
        .post("projects/datatag/", {
          name: this.name,
          tag_type: this.selectedTagType,
          unit:
            this.selectedTagType == TAG_TYPES.NUMBER_TYPE
              ? this.unit
              : undefined,
        })
        .then((reply) => {
          let tags = [reply.data, ...this.task.data_tags];
          this.$set(this.task, "data_tags", tags);
          this.show = false;
        });
    },
  },
};
</script>