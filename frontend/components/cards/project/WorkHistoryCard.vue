<template>
  <DefaultCardWithTitle title="Work history:">
    <v-layout column ma-0>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Amount</th>
              <th class="text-left">Beneficiary</th>
              <th class="text-left">Task</th>
              <th class="text-left">Time</th>
              <th class="text-left">Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="activity in activities" :key="activity.id">
              <td>{{ formattedReward(activity) }}</td>
              <td>
                {{
                  `${activity.beneficiary.first_name} ${activity.beneficiary.last_name}`
                }}
              </td>
              <td>{{ activity.task.action }}</td>
              <td>
                {{ $moment(activity.created).format("HH:mm YYYY-MM-DD") }}
              </td>
              <td @click="() => openExplorerLink(explorerSrc(activity))">
                <a><u>Explorer link</u></a>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-layout>
  </DefaultCardWithTitle>
</template>

<script>
export default {
  data() {
    return {
      activities: [],
    };
  },
  components: {
    DefaultCardWithTitle: () =>
      import("@/components/cards/DefaultCardWithTitle"),
  },
  methods: {
    formattedReward(value) {
      return `${parseFloat(value.task.reward)} USDC`;
    },
    explorerSrc(value) {
      return `https://testnet.algoexplorer.io/tx/${value.txid}`;
    },
    openExplorerLink(link) {
      window.open(link, "_blank");
    },
  },
  async fetch() {
    this.activities = await this.$axios(
      `projects/${this.$route.params.id}/activities/`
    ).then((reply) => reply.data.results);
  },
};
</script>

<style scoped>
th {
  font-size: 14px !important;
  color: var(--v-octonary-base) !important;
}
td {
  color: var(--v-nonary-base) !important;
}
a {
  color: var(--v-primary-base) !important;
}
</style>