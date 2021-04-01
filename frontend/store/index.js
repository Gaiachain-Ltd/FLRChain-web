export const state = () => ({
    regEmail: ''
})

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

    regEmail(state) {
        return state.regEmail;
    }
}

export const mutations = {

    setRegEmail(state, email) {
        state.regEmail = email;
    }
}

export const actions = {
    updateRegEmail({ commit }, email) {
        commit('setRegEmail', email);
    }
}