
export default {
    data() {
        return {
            firstNameRules: [
                (v) => !!v || "First name is required",
                (v) =>
                    (v && v.length <= 255) ||
                    "First name must be less than 255 characters",
            ],
            lastNameRules: [
                (v) => !!v || "Last name is required",
                (v) =>
                    (v && v.length <= 255) ||
                    "Last name must be less than 255 characters",
            ],
            emailRules: [
                (v) => {
                    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                    return (!v || pattern.test(v)) || 'Invalid e-mail.'
                }
            ],
            passwordRules: [
                (v) => !!v || "Password is required",
            ],
            requiredRules: [
                (v) => !!v || "Field is required",
            ],
            dateRules: [
                (v) => this.$moment(v, "YYYY-MM-DD").isValid() || "Incorrect format (YYYY-MM-DD)"
            ],
            decimalRules: [
                (v) => {
                    const pattern = /^[0-9]+\.?[0-9]{0,6}$/;
                    return pattern.test(v) || 'Invalid value';
                }
            ],
            nonZeroDecimalRules: [
                (v) => parseFloat(v) > 0.0 || "Value has to be greater than 0",
            ],
            oneOrMoreInteger: [
                (v) => parseInt(v) >= 1 || "Value has to be greater than 1"
            ],
            integerRules: [
                (v) => !isNaN(v) && (function(x) { return (x | 0) === x; })(parseFloat(v)) || "Invalid value"
            ],
            maxLengthRules(max=255) {
                return [
                    (v) => (!v || v.length <= max) || `Limit of ${max} characters exceeded.`
                ]
            }
        };
    },
};