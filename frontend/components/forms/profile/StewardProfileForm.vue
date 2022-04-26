<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <v-layout>
        <TextInput
          label="First name"
          v-model="value.first_name"
          :readonly="readonly"
        ></TextInput>
        <v-spacer></v-spacer>
        <TextInput
          label="Last name"
          v-model="value.last_name"
          :readonly="readonly"
        ></TextInput>
      </v-layout>
      <v-layout>
        <TextInput
          label="Email"
          v-model="value.email"
          :readonly="readonly"
        ></TextInput>
        <v-spacer></v-spacer>
        <TextInput
          label="Phone"
          v-model="value.phone"
          :readonly="readonly"
        ></TextInput>
      </v-layout>
      <TextInput
        label="Village"
        v-model="value.village"
        :readonly="readonly"
      ></TextInput>
    </v-layout>
  </v-form>
</template>

<script>
export default {
  props: {
    value: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>