<template>
  <DefaultProjectDelegate :project="project">
    <v-layout column ma-0>
      <v-layout row ma-0 mt-6>
        <v-flex xs6>
          <LabeledTextWithIcon
            label="Project start"
            :text="project.start"
            :icon="dateIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
        <v-flex xs6>
          <LabeledTextWithIcon
            label="Project end"
            :text="project.end"
            :icon="dateIcon"
          >
          </LabeledTextWithIcon>
        </v-flex>
      </v-layout>
      <v-flex v-if="description" mt-6>
        <DefaultText :size="14" :color="$vuetify.theme.themes.light.nonary">{{
          project.description
        }}</DefaultText>
      </v-flex>
    </v-layout>
  </DefaultProjectDelegate>
</template>

<script>
export default {
  props: {
    project: {},
    description: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dateIcon: require("@/assets/icons/date.svg"),
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    DefaultProjectDelegate: () =>
      import("@/components/delegates/DefaultProjectDelegate"),
    LabeledTextWithIcon: () => import("@/components/texts/LabeledTextWithIcon"),
  },
};
</script>