<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="activities"
      no-data-text="No progress"
      hide-default-footer
      :items-per-page="-1"
    >
      <template v-slot:item.name="{ item }">
        <StewardCell
          :profile="{ name: item.name, id: item.user_id }"
        ></StewardCell>
      </template>
      <template v-slot:item.amount="{ item }">
        {{ amount(item) }}
      </template>
      <template v-slot:item.round-time="{ item }">
        {{ datetime(item) }}
      </template>
      <template v-slot:item.details="{ item }">
        <v-layout @click.prevent="() => openExplorerTransactionLink(item.txid)">
          <a href="">See more</a>
        </v-layout>
      </template>
      <template v-slot:item.data="{ item }">
        <SubmittedDataCell
          v-if="item.activity_type == 0"
          :data="item"
        ></SubmittedDataCell>
      </template>
      <template v-slot:item.photos="{ item }">
        <v-layout
          shrink
          style="cursor: pointer"
          @click.prevent="() => onShowPopup(item)"
        >
          <DefaultSVGIcon
            :icon="item.photos > 0 ? photosIcon : noPhotosIcon"
          ></DefaultSVGIcon>
        </v-layout>
      </template>
    </v-data-table>
    <PhotoGalleryPopup
      v-if="showPopup"
      v-model="showPopup"
      :activity="activityToShow"
    ></PhotoGalleryPopup>
  </div>
</template>

<script>
import AlgoExplorerMixin from "@/mixins/AlgoExplorerMixin";
import { APPROVAL } from "@/constants/project";

export default {
  mixins: [AlgoExplorerMixin],
  props: {
    project: {},
  },
  data() {
    return {
      showPopup: false,
      activityToShow: null,
      activities: [],
      photosIcon: require("@/assets/icons/photos.svg"),
      noPhotosIcon: require("@/assets/icons/no-photos.svg"),
      headers: [
        {
          text: "Steward",
          value: "name",
        },
        {
          text: "Task",
          value: "task_name",
        },
        {
          text: "Amount",
          value: "amount",
        },
        {
          text: "Data",
          value: "data",
          sortable: false,
        },
        {
          text: "Photos",
          value: "photos",
        },
        {
          text: "Date",
          value: "round-time",
        },
        {
          text: "Details",
          value: "details",
          sortable: false,
        },
      ],
    };
  },
  components: {
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
    PhotoGalleryPopup: () =>
      import("@/components/popups/projects/PhotoGalleryPopup"),
    SubmittedDataCell: () =>
      import("@/components/tables/projects/SubmittedDataCell"),
    StewardCell: () => import("@/components/tables/projects/StewardCell"),
  },
  methods: {
    amount(item) {
      return `${item.amount} USDC`;
    },
    datetime(item) {
      return this.$moment.unix(item["round-time"]).format("YYYY-MM-DD HH:mm");
    },
    onShowPopup(activity) {
      if (activity.photos > 0) {
        this.activityToShow = activity;
        this.showPopup = true;
      }
    },
  },
  async fetch() {
    this.activities = await this.$axios
      .get(
        `projects/${this.project.id}/activities/?status=${APPROVAL.ACCEPTED}`
      )
      .then((reply) => reply.data);
  },
};
</script>