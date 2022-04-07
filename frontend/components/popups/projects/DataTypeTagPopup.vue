<template>
  <DefaultPopup :show.sync="show">
    <v-flex slot="icon"> </v-flex>
    <v-flex slot="content" ma-6>
      <v-form ref="form">
        <v-layout column>
          <DefaultText :color="$vuetify.theme.themes.light.primary"
            >Add new type</DefaultText
          >
          <TextInput
            class="mt-3"
            label="Type name"
            placeholder="Please enter tag type name..."
            v-model="name"
            :rules="[...maxLengthRules()]"
          ></TextInput>
        </v-layout>
      </v-form>
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
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
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
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultPopup: () => import("@/components/popups/DefaultPopup"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
  methods: {
    async handleAdd() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        await this.$axios
          .post("projects/datatypetag/", { name: this.name })
          .then((reply) => {
            this.$set(this.task, "data_type_tag", reply.data);
            this.show = false;
          });
      }
    },
  },
};
</script>