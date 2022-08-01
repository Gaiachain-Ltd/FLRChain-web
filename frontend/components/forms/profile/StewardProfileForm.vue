<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <v-layout>
        <v-flex xs5>
          <v-layout column>
            <DefaultText :size="12"> First name </DefaultText>
            <DefaultText :size="14" class="mt-1 text-wrap" color="#a6a6a6">{{
              value.first_name
            }}</DefaultText>
          </v-layout>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <v-layout column>
            <DefaultText :size="12"> Last name </DefaultText>
            <DefaultText :size="14" class="mt-1 text-wrap" color="#a6a6a6">{{
              value.last_name
            }}</DefaultText>
          </v-layout>
        </v-flex>
      </v-layout>
      <v-layout class="mt-3">
        <v-flex xs5>
          <v-layout column>
            <DefaultText :size="12"> Email </DefaultText>
            <DefaultText :size="14" class="mt-1 text-wrap" color="#a6a6a6">{{
              value.email
            }}</DefaultText>
          </v-layout>
        </v-flex>
        <v-spacer></v-spacer>
        <v-flex xs5>
          <v-layout column>
            <DefaultText :size="12"> Phone </DefaultText>
            <DefaultText :size="14" class="mt-1 text-wrap" color="#a6a6a6">{{
              value.phone
            }}</DefaultText>
          </v-layout>
        </v-flex>
      </v-layout>
      <v-layout column class="mt-3">
        <DefaultText :size="12"> Village </DefaultText>
        <DefaultText :size="14" class="mt-1 text-wrap" color="#a6a6a6">{{
          value.village
        }}</DefaultText>
      </v-layout>
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
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>