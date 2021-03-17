export const getters = {
    isAuthenticated(state) {
        return state.auth.loggedIn
    },

    loggedInUser(state) {
        return state.auth.user
    },

    isFacililator(state) {
        return state.auth.user.type === 1;
    },

    isInvestor(state) {
        return state.auth.user.type === 2;
    },
}