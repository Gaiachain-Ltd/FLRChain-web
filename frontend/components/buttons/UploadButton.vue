<template>
  <v-layout column shrink align-end>
    <v-layout style="width: 100%" mb-3>
      <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary"
        >Project image</DefaultText
      >
    </v-layout>
    <v-img :src="source" max-height="300"></v-img>
    <v-layout shrink mt-3>
      <input
        ref="file"
        type="file"
        accept="image/png,image/jpeg"
        style="display: none"
        @change="onChangeFile"
      />
      <ActionButton
        color="primary"
        @click.prevent="selectFile"
        :disabled="readonly"
        >Upload file</ActionButton
      >
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      selectedFile: null,
      loading: false,
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  computed: {
    source() {
      if (this.selectedFile) {
        return URL.createObjectURL(this.selectedFile);
      } else if (this.project.image) {
        return `${this.$config.baseUrl}/${this.project.image}`;
      } else {
        return require("@/assets/images/placeholder.png");
      }
    },
  },
  methods: {
    selectFile() {
      this.$refs.file.click();
    },
    onChangeFile(file) {
      this.selectedFile = file.target.files[0];
      if (!this.project.id) {
        this.$set(this.project, "fileToUpload", this.selectedFile);
      } else {
        this.uploadFile();
      }
    },
    uploadFile(updateProject = false) {
      this.loading = true;
      let formData = new FormData();
      formData.append("image", this.selectedFile);
      this.$axios
        .put(`projects/${this.project.id}/image/`, formData)
        .then((reply) => {
          if (updateProject) {
            this.$emit("update:project", reply.data);
          }
          this.loading = false;
        })
        .catch(error => {
          console.log("ERROR", error);
        });
    },
  },
};
</script>