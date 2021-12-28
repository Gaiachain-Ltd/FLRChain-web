<script>
export default {
  data() {
    return {
      loading: false,
      message: "",
      snackBarVisible: false,
      snackBarPositive: false,
    };
  },
  methods: {
    beforeRequest() {
      this.loading = true;
    },
    onSuccess(message = "") {
      this.loading = false;
      if (message) {
        this.message = message;
        this.snackBarPositive = true;
        this.snackBarVisible = true;
      }
    },
    onError(message = "") {
      this.loading = false;
      if (message) {
        this.message = message;
        this.snackBarPositive = false;
        this.snackBarVisible = true;
      }
    },
  },
};
</script>