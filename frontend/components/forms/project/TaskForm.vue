<template>
  <v-form ref="form">
    <v-layout column ma-0>
      <v-layout row ma-0 mb-3>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          `Task #${index + 1}`
        }}</DefaultText>
        <v-spacer></v-spacer>
        <DefaultIconButton
          v-if="index != 0"
          :config="deleteBtnConf"
          @clicked="$emit('delete', index)"
        ></DefaultIconButton>
      </v-layout>
      <v-layout row ma-0>
        <v-flex xs9>
          <TextInput
            label="Action*"
            :text.sync="task.action"
            placeholder="Please enter action..."
            :rules="requiredRules"
            required
          ></TextInput>
        </v-flex>
        <v-flex ml-6>
          <TextInput
            label="Reward*"
            :text.sync="task.reward"
            :rules="[...requiredRules, ...decimalRules]"
            required
          ></TextInput>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    task: {},
    index: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      deleteBtnConf: {
        iconOn: require("@/assets/icons/remove.svg"),
        label: "Delete",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.error,
      },
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>