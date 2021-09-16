export const state = () => ({
    regEmail: '',
    drawerState: null,
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
    },
    getDrawerState(state) {
      return state.drawerState
    },
}

export const mutations = {
    setRegEmail(state, email) {
        state.regEmail = email;
    },
    setDrawerState(state,value) {
      state.drawerState = value;
    },
}

export const actions = {
    updateRegEmail({ commit }, email) {
        commit('setRegEmail', email);
    },
    updateDrawerState({ commit }, value) {
        commit('setDrawerState', value);
    },
}
