<template>
  <v-menu
    v-model="showMenu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    offset-overflow
    bottom
    :nudge-bottom="-30"
    max-width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-layout column>
        <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
          label
        }}</DefaultText>
        <v-text-field
          class="text-field-style"
          :background-color="readonly ? 'white' : '#f7f9fb'"
          height="50"
          v-model="date"
          v-bind="attrs"
          v-on="on"
          @click.prevent="showMenu = showMenu"
          :solo="!readonly"
          :disabled="readonly"
          flat
          readonly
          :required="required"
          :rules="rules"
        >
          <v-layout
            column
            pr-2
            mb-1
            align-center
            slot="prepend-inner"
            @click="showMenu = !showMenu"
          >
            <DefaultSVGIcon
              :class="readonly && 'readonly-icon'"
              :icon="require('@/assets/icons/calendar.svg')"
            ></DefaultSVGIcon>
          </v-layout>
        </v-text-field>
      </v-layout>
    </template>
    <v-date-picker
      v-model="date"
      no-title
      color="primary"
      :min="minimumDate"
      @input="showMenu = false"
    ></v-date-picker>
  </v-menu>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
    },
    label: {
      type: String,
      default: "",
    },
    required: {
      type: Boolean,
      default: false,
    },
    rules: {
      type: Array,
      default: () => [],
    },
    readonly: {
      type: Boolean,
      default: false
    },
    min: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      showMenu: false,
    };
  },
  watch: {
    min() {
      if (!this.min) {
        return;
      }
      const min = this.$moment(this.min, "YYYY-MM-DD");
      const current = this.$moment(this.date, "YYYY-MM-DD");
      if (min > current) {
        this.date = min.format("YYYY-MM-DD");
      }
    }
  },
  computed: {
    date: {
      get() {
        return this.text;
      },
      set(value) {
        this.$emit("update:text", value);
      },
    },
    minimumDate() {
      if (this.min == "") {
        return this.$moment().format("YYYY-MM-DD");
      } else {
        return this.min;
      }
    }
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped>
.text-field-style {
  border-radius: 7px !important;
}
.readonly-icon {
  margin-top: 8px !important;
}
</style>