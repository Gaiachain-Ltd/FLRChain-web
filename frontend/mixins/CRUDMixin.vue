<script>
export default {
  data() {
    return {
      loading: false,
      message: "",
      showSuccessPopup: false,
      showErrorPopup: false,
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
        this.showSuccessPopup = true;
      }
    },
    onError(message = "") {
      this.loading = false;
      if (message) {
        this.message = message;
        this.showErrorPopup = true;
      }
    },
  },
};
</script>