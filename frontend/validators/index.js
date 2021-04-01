
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
                (v) => !!v || "Email is required",
                (v) => {
                    const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                    return pattern.test(v) || 'Invalid e-mail.'
                }
            ],
            passwordRules: [
                (v) => !!v || "Password is required",
            ]
        };
    },
};